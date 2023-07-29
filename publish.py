import pika
import uuid
import json

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.exchange_declare(
    exchange='order',
    exchange_type='direct'
)

order = {
    "id": str(uuid.uuid4()),
    "user_email": "jasur@gmail.com",
    "product": "Product 1",
    "quantity": 3
}

channel.basic_publish(
    exchange='order',
    routing_key='order.notify',
    body=json.dumps({'user_email': order['user_email']})
)
print('* [x] Sent notify message')

channel.basic_publish(
    exchange='order',
    routing_key='order.report',
    body=json.dumps(order)
)
print('* [x] Sent report message')
connection.close()
