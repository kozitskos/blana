from fastapi import FastAPI
import socketio

app = FastAPI()
sio = socketio.AsyncServer(async_mode='asgi', cors_allowed_origins="*")
socket_app = socketio.ASGIApp(sio, other_asgi_app=app, socketio_path='/ws/socket.io')

# Mount the socket.io app
app.mount("/ws", socket_app)

@sio.event
async def connect(sid, environ):
    print("Client connected:", sid)

@sio.event
async def disconnect(sid):
    print("Client disconnected:", sid)

@sio.event
async def message(sid, data):
    print("Received message:", data)
    await sio.emit('response', data, to=sid)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
