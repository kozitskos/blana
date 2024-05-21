import pika
import time

def callback(ch, method, properties, body):
    message = body.decode()
    print(f"Received {message}")
    # Здесь должна быть логика обработки сообщения
    time.sleep(5)  # Имитация длительной обработки

    response = f"Processed {message}"
    
    # Отправка результата обратно в очередь
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue=properties.reply_to, durable=True)
    channel.basic_publish(
        exchange='',
        routing_key=properties.reply_to,
        body=response,
        properties=pika.BasicProperties(
            correlation_id=properties.correlation_id,
            delivery_mode=2,  # Сохранить сообщение
        )
    )
    connection.close()

    ch.basic_ack(delivery_tag=method.delivery_tag)

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='task_queue', durable=True)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='task_queue', on_message_callback=callback)

print('Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
