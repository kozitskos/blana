import pika
import time
import random
import base64
import tempfile
from concurrent.futures import ThreadPoolExecutor, TimeoutError
from faster_whisper import WhisperModel

class TaskProcessor:
    def __init__(self, queue_name='task_queue', rabbitmq_host='localhost'):
        self.queue_name = queue_name
        self.rabbitmq_host = rabbitmq_host
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(self.rabbitmq_host))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.queue_name, durable=True)
        self.channel.basic_qos(prefetch_count=1)
        
        self.model = WhisperModel("base", device="cpu", compute_type="int8")

    def process_task(self, body):
        print(f" [x] Received task")

        # Decode the base64 audio data
        audio_data = base64.b64decode(body)

        # Save the binary data to a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".m4a") as temp_audio_file:
            temp_audio_file.write(audio_data)
            temp_audio_path = temp_audio_file.name

        try:
            # Transcribe the temporary audio file
            segments, _ = self.model.transcribe(temp_audio_path, beam_size=5, language="ru", condition_on_previous_text=True)
            transcription = " ".join([segment.text for segment in segments])

            print(f" [x] Transcription done: {transcription}")
            return f"Processed: {transcription}"
        finally:
            # Ensure the temporary file is removed
            import os
            os.remove(temp_audio_path)

    def send_response(self, response, properties):
        connection = pika.BlockingConnection(pika.ConnectionParameters(self.rabbitmq_host))
        channel = connection.channel()
        channel.queue_declare(queue=properties.reply_to, durable=True)
        channel.basic_publish(
            exchange='',
            routing_key=properties.reply_to,
            body=response,
            properties=pika.BasicProperties(
                delivery_mode=2,  # Persist message
            )
        )
        connection.close()

    def callback(self, ch, method, properties, body):
        delivery_tag = method.delivery_tag

        with ThreadPoolExecutor(max_workers=1) as executor:
            future = executor.submit(self.process_task, body)
            try:
                # Wait for the task to complete within 10 seconds
                response = future.result(timeout=30)
                
                # Send response if reply_to is specified
                if properties.reply_to:
                    self.send_response(response, properties)
                # Acknowledge the message if the task is done within the timeout
                ch.basic_ack(delivery_tag=delivery_tag)
            except TimeoutError:
                print(f" [x] Task timed out, requeuing {body}")
                # Requeue the message if the task is not done within the timeout
                ch.basic_nack(delivery_tag=delivery_tag, requeue=True)
            except Exception as e:
                print(f" [x] Task failed with exception: {e}, requeuing {body}")
                # Requeue the message if the task raises an exception
                ch.basic_nack(delivery_tag=delivery_tag, requeue=True)

    def start_consuming(self):
        self.channel.basic_consume(queue=self.queue_name, on_message_callback=self.callback)
        print(' [*] Waiting for messages. To exit press CTRL+C')
        self.channel.start_consuming()

    def close_connection(self):
        self.connection.close()

if __name__ == "__main__":
    processor = TaskProcessor(queue_name='task_queue')
    try:
        processor.start_consuming()
    except KeyboardInterrupt:
        processor.close_connection()
        print('Connection closed')
