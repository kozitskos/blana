import socketio
import time
import requests

# Define the server URL and endpoints
SERVER_URL = 'http://localhost:8000'
LOGIN_ENDPOINT = f'{SERVER_URL}/auth/token'
WEBSOCKET_URL = f'{SERVER_URL}/ws/socket.io'

# User credentials
USERNAME = 'jhonedoe'
PASSWORD = 'jhonedoe'

# Note ID to be used
NOTE_ID = 'e4259a69-3089-4d33-9dcf-af7390b1f532'

# Messages to send
messages = ["Hello, server!", "How are you?", "What's the time?", "Goodbye!"]

# Function to get JWT token
def get_jwt_token():
    response = requests.post(LOGIN_ENDPOINT, data={'username': USERNAME, 'password': PASSWORD})
    response.raise_for_status()
    # print(response.text)
    return response.json()['access_token']
    # return response.text

# Function to create a new socket.io client and connect to the server
def create_client(token):
    sio = socketio.Client()

    @sio.event
    def connect():
        print("Connected to server")
        # Send note ID after connecting
        sio.emit('set_note_id', {'note_id': NOTE_ID})
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
            sio.emit('message', {'audio': message})
            current_message_index += 1
        else:
            sio.disconnect()

    return sio

# Authenticate and get the JWT token
token = get_jwt_token()
print(token)

# Create and configure the socket.io client
sio = create_client(token)

# Set the initial message index
current_message_index = 0

# Connect to the WebSocket with the token
sio.connect(WEBSOCKET_URL, headers={'Authorization': f'Bearer {token}'}, socketio_path='/ws/socket.io')
sio.wait()
