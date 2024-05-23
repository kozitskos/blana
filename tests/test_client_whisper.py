import socketio
import time
import pickle

sio = socketio.Client()

# Load Base64 audio from pickle file
with open("audio_base64.pkl", "rb") as pkl_file:
    base64_audio = pickle.load(pkl_file)

messages = [base64_audio] * 4  # Repeat the base64 audio 4 times
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
        print(f"Sending message: {message[:50]}...")  # Print the first 50 chars to avoid clutter
        sio.send(message)
        current_message_index += 1
    else:
        sio.disconnect()

sio.connect('http://localhost:8000', socketio_path='/ws/socket.io')
sio.wait()
