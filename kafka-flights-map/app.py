from flask import Flask, render_template, Response
from pykafka import KafkaClient
import os

def get_kafka_client():
    KAFKA_BROKER_URL = os.getenv('KAFKA_BROKER_URL', '127.0.0.1:9092')
    try:
        print(f"Connecting to Kafka at {KAFKA_BROKER_URL}")
        return KafkaClient(hosts=KAFKA_BROKER_URL)
    except Exception as e:
        print(f"Failed to connect to Kafka: {e}")
        return None

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/topic/<topicname>')
def get_messages(topicname):
    # Kafka Consumer
    client = get_kafka_client()
    def events():
        for i in client.topics[topicname].get_simple_consumer():
            yield 'data:{0}\n\n'.format(i.value.decode())
    return Response(events(), mimetype='text/event-stream')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=os.getenv('FLASK_DEBUG', 'False'), port=5001)