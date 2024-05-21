import pika
import time
import random
from concurrent.futures import ThreadPoolExecutor, TimeoutError

def process_task(body):
    print(f" [x] Received {body}")
    work_time = random.randint(1, 10)
    print(f" [x] Will be proceed in {work_time} seconds")
    time.sleep(work_time)
    print(f" [x] Done in {work_time} seconds")
    return True

def callback(ch, method, properties, body):
    delivery_tag = method.delivery_tag

    with ThreadPoolExecutor(max_workers=1) as executor:
        future = executor.submit(process_task, body)
        try:
            # Wait for the task to complete within 10 seconds
            future.result(timeout=5)
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

# Establish connection with RabbitMQ server
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Declare the durable queue
channel.queue_declare(queue='task_queue', durable=True)

# Set prefetch count to 1
channel.basic_qos(prefetch_count=1)

# Start consuming messages from the queue with the callback function
channel.basic_consume(queue='task_queue', on_message_callback=callback)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
