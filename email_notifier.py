from flask import Flask, make_response, request
import os
import secrets
import pika

app = Flask(__name__)
app.secret_key = secrets.token_urlsafe(16)

@app.route("/")
def healthcheck():
    return make_response("OK", 200)

@app.route('/send_email', methods=['POST'])
def send_email():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='email')
    channel.basic_publish(
        exchange='',
        routing_key='email',
        body=request.get_json()
    )
    
    return make_response("OK", 200) 

if __name__ == '__main__':
    app.run(
        host=os.getenv("APP_HOST"), 
        port=os.getenv("SENDER_PORT"), 
        debug=True
    )