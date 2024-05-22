import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Declare a durable queue
channel.queue_declare(queue='task_queue', durable=True)

# Publish messages to the queue
for i in range(100):
    message = f'Task {i+1}'
    channel.basic_publish(
        exchange='',
        routing_key='task_queue',
        body=message,
        properties=pika.BasicProperties(
            delivery_mode=2,
            reply_to='task_queue'  # make message persistent
        ))
    print(f" [x] Sent {message}")

connection.close()
