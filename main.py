from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import socketio
import aio_pika
import asyncio

app = FastAPI()
sio = socketio.AsyncServer(async_mode='asgi', cors_allowed_origins="*")
socket_app = socketio.ASGIApp(sio, other_asgi_app=app, socketio_path='/ws/socket.io')

# Mount the socket.io app
app.mount("/ws", socket_app)

# Serve the static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Connection parameters for RabbitMQ
RABBITMQ_URL = "amqp://guest:guest@localhost/"

# Queue names
REQUEST_QUEUE = "task_queue"
RESPONSE_QUEUE = "response_queue"

# Global variable for the RabbitMQ connection
rabbitmq_connection = None

async def setup_rabbitmq():
    global rabbitmq_connection
    rabbitmq_connection = await aio_pika.connect_robust(RABBITMQ_URL)
    channel = await rabbitmq_connection.channel()
    await channel.declare_queue(REQUEST_QUEUE, durable=True)
    await channel.declare_queue(RESPONSE_QUEUE, durable=True)

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

@sio.event
async def disconnect(sid):
    print("Client disconnected:", sid)

@sio.event
async def message(sid, data):
    print("Received message:", data)
    await send_message(data)
    await receive_message(sid)

async def send_message(message):
    async with rabbitmq_connection.channel() as channel:
        # Publish the message to the request queue
        await channel.default_exchange.publish(
            aio_pika.Message(
                body=message.encode(),
                delivery_mode=aio_pika.DeliveryMode.PERSISTENT,  # Persist message
                reply_to=RESPONSE_QUEUE
            ),
            routing_key=REQUEST_QUEUE
        )

async def receive_message(sid):
    async with rabbitmq_connection.channel() as channel:
        # Consume the message from the response queue
        response_queue = await channel.declare_queue(RESPONSE_QUEUE, durable=True)
        async with response_queue.iterator() as queue_iter:
            async for message in queue_iter:
                async with message.process():
                    response = message.body.decode()
                    await sio.emit('response', response, to=sid)
                    return

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
