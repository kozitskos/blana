import socketio
import time

sio = socketio.Client()

messages = ["Hello, server!", "How are you?", "What's the time?", "Goodbye!"]
current_message_index = 0

@sio.event
def connect():
    print("Connected to server")
    send_next_message()

@sio.event
def response(data):
    print("Message from server:", data)
    send_next_message()

@sio.event
def disconnect():
    print("Disconnected from server")

def send_next_message():
    global current_message_index
    if current_message_index < len(messages):
        message = messages[current_message_index] + " " + str(time.time())
        print(f"Sending message: {message}")
        sio.send(message)
        current_message_index += 1
    else:
        sio.disconnect()

sio.connect('http://localhost:8000', socketio_path='/ws/socket.io')
sio.wait()
