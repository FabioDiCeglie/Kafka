from pykafka import KafkaClient
import json
from datetime import datetime
import uuid
import time
import os

KAFKA_BROKER_URL = os.getenv('KAFKA_BROKER_URL', '127.0.0.1:9092')

#KAFKA PRODUCER
try:
    print(f"Connecting to Kafka at {KAFKA_BROKER_URL}")
    client = KafkaClient(hosts=KAFKA_BROKER_URL)
    topic = client.topics['flightdata']
    producer = topic.get_sync_producer()
except Exception as e:
    print(f"Failed to connect to Kafka: {e}")
    exit()

#GENERATE UUID
def generate_uuid():
    return uuid.uuid4()

#CONSTRUCT MESSAGE AND SEND IT TO KAFKA
data = {}

def generateCurrentLocation(coordinates, airline, flight, current_index):
    data['airline'] = airline
    data['flight'] = flight
    data['key'] = data['airline'] + '_' + str(generate_uuid())
    data['timestamp'] = str(datetime.utcnow())
    data['latitude'] = coordinates[current_index][1]
    data['longitude'] = coordinates[current_index][0]
    message = json.dumps(data)
    print("message: ", message)
    try:
        producer.produce(message.encode('ascii'))
    except Exception as e:
        print(f"Error Type: {type(e)}")
        print(f"Error Repr: {repr(e)}")
        print(f"Error: {e}")
    time.sleep(0.5)

    # Calculate next index
    next_index = current_index + 1
    if next_index == len(coordinates):
        next_index = 0  # Reset to start from the beginning
    return next_index

if __name__ == "__main__":
    files_data = []
    for flight_info in [{'file': 'flight1.json', 'airline': 'Ryanair', 'flight': 'RYR50HA'}, {'file': 'flight2.json', 'airline': 'Lufthansa', 'flight': 'LH500'}]:
        input_file = open('./data/' + flight_info['file'])
        json_array = json.load(input_file)
        coordinates = json_array['features'][0]['geometry']['coordinates']
        files_data.append({
            'coordinates': coordinates,
            'airline': flight_info['airline'],
            'flight': flight_info['flight'],
            'current_index': 0
        })

    while True:
        for flight_data in files_data:
            next_idx = generateCurrentLocation(
                flight_data['coordinates'],
                flight_data['airline'],
                flight_data['flight'],
                flight_data['current_index']
            )
            flight_data['current_index'] = next_idx