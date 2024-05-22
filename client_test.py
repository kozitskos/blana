import socketio
import time 

sio = socketio.Client()

@sio.event
def connect():
    print("Connected to server")
    sio.send("Hello, server!" +" " +str(time.time()))

@sio.event
def response(data):
    print("Message from server:", data)
    sio.disconnect()

@sio.event
def disconnect():
    print("Disconnected from server")

sio.connect('http://localhost:8000', socketio_path='/ws/socket.io')
sio.wait()
