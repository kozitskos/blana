import pika
import time
import random
from concurrent.futures import ThreadPoolExecutor, TimeoutError

class TaskProcessor:
    def __init__(self, queue_name='task_queue', rabbitmq_host='localhost'):
        self.queue_name = queue_name
        self.rabbitmq_host = rabbitmq_host
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(self.rabbitmq_host))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.queue_name, durable=True)
        self.channel.basic_qos(prefetch_count=1)

    def process_task(self, body):
        print(f" [x] Received {body}")
        work_time = random.randint(1, 1)
        print(f" [x] Will be processed in {work_time} seconds")
        time.sleep(work_time)
        print(f" [x] Done in {work_time} seconds")
        return f"Processed {body.decode()}"

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
                response = future.result(timeout=5)
                
                # Send response if reply_to is specified
                
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
