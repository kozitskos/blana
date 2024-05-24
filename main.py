from fastapi import FastAPI, Depends, HTTPException
# from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
import socketio
import aio_pika
import asyncio
from uuid import UUID

from app import schemas, crud, models
from app.database import engine, SessionLocal
from app.deps import get_current_user
from app.routers import auth, notes, feedback, summaries

app = FastAPI()
sio = socketio.AsyncServer(async_mode='asgi', cors_allowed_origins="*")
socket_app = socketio.ASGIApp(sio, other_asgi_app=app, socketio_path='/ws/socket.io')

# Mount the socket.io app
app.mount("/ws", socket_app)

# Serve the static files
# app.mount("/static", StaticFiles(directory="static"), name="static")

# Connection parameters for RabbitMQ
RABBITMQ_URL = "amqp://guest:guest@localhost/"

# Queue names
REQUEST_QUEUE = "task_queue"
RESPONSE_QUEUE_PREFIX = "response_queue_"

# Global variable for the RabbitMQ connection
rabbitmq_connection = None

async def setup_rabbitmq():
    global rabbitmq_connection
    rabbitmq_connection = await aio_pika.connect_robust(RABBITMQ_URL)
    channel = await rabbitmq_connection.channel()
    await channel.declare_queue(REQUEST_QUEUE, durable=True)

@app.on_event("startup")
async def on_startup():
    await setup_rabbitmq()

@app.on_event("shutdown")
async def on_shutdown():
    if rabbitmq_connection:
        await rabbitmq_connection.close()

@sio.event
async def connect(sid, environ):
    print("Client connected:", sid)
    await create_response_queue(sid)

@sio.event
async def disconnect(sid):
    print("Client disconnected:", sid)
    await delete_response_queue(sid)

@sio.event
async def message(sid, data):
    print("Received message:", data)
    note_id = UUID(data['note_id'])
    audio_data = data['audio']
    await send_message(audio_data, sid)
    await receive_message(sid, note_id)

async def create_response_queue(sid):
    async with rabbitmq_connection.channel() as channel:
        await channel.declare_queue(RESPONSE_QUEUE_PREFIX + sid, durable=True)

async def delete_response_queue(sid):
    async with rabbitmq_connection.channel() as channel:
        await channel.queue_delete(RESPONSE_QUEUE_PREFIX + sid)

async def send_message(message, sid):
    async with rabbitmq_connection.channel() as channel:
        # Publish the message to the request queue
        await channel.default_exchange.publish(
            aio_pika.Message(
                body=message.encode(),
                delivery_mode=aio_pika.DeliveryMode.PERSISTENT,  # Persist message
                reply_to=RESPONSE_QUEUE_PREFIX + sid
            ),
            routing_key=REQUEST_QUEUE
        )

async def receive_message(sid, note_id):
    async with rabbitmq_connection.channel() as channel:
        # Consume the message from the response queue
        response_queue = await channel.declare_queue(RESPONSE_QUEUE_PREFIX + sid, durable=True)
        async with response_queue.iterator() as queue_iter:
            async for message in queue_iter:
                async with message.process():
                    response = message.body.decode()
                    await sio.emit('response', response, to=sid)
                    await update_note_content(note_id, response)
                    return

async def update_note_content(note_id: UUID, content: str):
    async with SessionLocal() as db:
        await asyncio.get_event_loop().run_in_executor(None, crud.update_note_content, db, note_id, content)

# Include the routers
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(notes.router, prefix="/notes", tags=["notes"])
app.include_router(feedback.router, prefix="/feedback", tags=["feedback"])
app.include_router(summaries.router, prefix="/summary", tags=["summary"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
