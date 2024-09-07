import socketio
import aio_pika
from sqlalchemy.orm import Session
from uuid import UUID
import asyncio
from app import schemas, crud, models
from app.database import SessionLocal
from app.deps import get_current_user


sio = socketio.AsyncServer(async_mode='asgi', cors_allowed_origins="*")

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

@sio.event
async def connect(sid, environ):
    auth = environ.get('HTTP_AUTHORIZATION', None)
    if auth is None:
        await sio.disconnect(sid)
        return
    token = auth.replace('Bearer ', '')
    db: Session = SessionLocal()
    try:
        print('connect ', sid)
        if not token:
            await sio.disconnect(sid)
            return
        
        user = get_current_user(db, token)
        if user:
            await sio.save_session(sid, {'user_id': user.id})
            await create_response_queue(sid)
            print(f'user {user.id} connected')
        else:
            await sio.disconnect(sid)
    finally:
        db.close()

# @sio.event
# async def connect(sid, environ):
#     print("Client connected:", sid)
#     await create_response_queue(sid)

# @sio.event
# async def connect(sid, environ, auth):
#     db: Session = SessionLocal()
#     try:
#         print('connect ', sid)
#         print(auth)
#         token = auth.get('token', '').replace('Bearer ', '')
#         # print(token)
#         if not token:
#             await sio.disconnect(sid)
#             return
        
#         user = get_current_user(db, token)
#         if user:
#             await sio.save_session(sid, {'user_id': user.id})
#             await create_response_queue(sid)
#             print(f'user {user.id} connected')
#         else:
#             await sio.disconnect(sid)
#     finally:
#         db.close()

# @sio.event
# async def connect(sid, environ, auth):
#     if auth is None:
#         await sio.disconnect(sid)
#         return
#     db: Session = SessionLocal()
#     try:
#         print('connect ', sid)
#         token = auth.get('token', '').replace('Bearer ', '')
#         if not token:
#             await sio.disconnect(sid)
#             return
        
#         user = get_current_user(db, token)
#         if user:
#             await sio.save_session(sid, {'user_id': user.id, 'username': user.username})
#             db.query(models.User).filter(models.User.id == user.id).update({models.User.online: True})
#             db.commit()
#             print(f'user {user.id} connected')
#         else:
#             await sio.disconnect(sid)
#     finally:
#         db.close()

@sio.event
async def disconnect(sid):
    print("Client disconnected:", sid)
    await delete_response_queue(sid)

@sio.event
async def set_note_id(sid, data):
    print('Received note_id:', data)
    db: Session = SessionLocal()
    try:
        session = await sio.get_session(sid)
        user_id = session.get('user_id')
        note_id = data.get('note_id')
        
        if not note_id or not user_id:
            await sio.disconnect(sid)
            return

        note = crud.get_note_by_id(db, UUID(note_id))
        if not note or note.owner_id != user_id:
            await sio.disconnect(sid)
            return

        session['note_id'] = str(note.id)  # Ensure the note_id is stored as a string
        await sio.save_session(sid, session)
        print(f'Note {note.id} associated with user {user_id}')
    finally:
        db.close()

# @sio.event
# async def message(sid, data):
#     print("Received message:", data)
#     note_id = UUID(data['note_id'])
#     audio_data = data['audio']
#     await send_message(audio_data, sid)
#     await receive_message(sid, note_id)

@sio.event
async def message(sid, data):
    print('Received message:', data)
    session = await sio.get_session(sid)
    user_id = session.get('user_id')
    note_id = session.get('note_id')
    
    if not note_id or not user_id:
        await sio.disconnect(sid)
        return

    audio_data = data['audio']
    await send_message(audio_data, sid)
    await receive_message(sid, UUID(note_id))

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
    db: Session = SessionLocal()
    try:
        await asyncio.get_event_loop().run_in_executor(None, crud.update_note_content, db, note_id, content)
    finally:
        db.close()
