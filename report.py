import pika
import json

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

queue = channel.queue_declare('order_report')
queue_name = queue.method.queue

channel.queue_bind(
    exchange='order',
    queue=queue_name,
    routing_key='order.report'
)


def callback(ch, method, properties, body):
    payload = json.loads(body)
    print(' [x] Generating report')
    print(f"""
     Order ID: {payload['id']}
     User Email: {payload['user_email']}
     Product: {payload['product']}
     Quantity: {payload['quantity']}           
    """)
    print(f" [x] Done!")
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_consume(on_message_callback=callback, queue=queue_name)

print(" [*] Waiting for messages. To exit press CTRL+C")
channel.start_consuming()
