import asyncio
import json
import uuid
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import pika

app = FastAPI()

class ConnectionManager:
    def __init__(self):
        self.active_connections = {}

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections[websocket] = str(uuid.uuid4())

    def disconnect(self, websocket: WebSocket):
        del self.active_connections[websocket]

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    
    # Установка соединения с RabbitMQ
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='task_queue', durable=True)

    response_queue = f'response_queue_{uuid.uuid4()}'
    channel.queue_declare(queue=response_queue, durable=True)
    
    def callback(ch, method, properties, body):
        if properties.correlation_id == manager.active_connections[websocket]:
            asyncio.run(manager.send_personal_message(body.decode(), websocket))
            ch.basic_ack(delivery_tag=method.delivery_tag)
            channel.stop_consuming()

    channel.basic_consume(queue=response_queue, on_message_callback=callback)

    try:
        while True:
            data = await websocket.receive_text()
            correlation_id = manager.active_connections[websocket]
            channel.basic_publish(
                exchange='',
                routing_key='task_queue',
                body=data,
                properties=pika.BasicProperties(
                    delivery_mode=2,
                    correlation_id=correlation_id,
                    reply_to=response_queue
                )
            )
            channel.start_consuming()
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    finally:
        connection.close()
