from pykafka import KafkaClient
import json
from datetime import datetime
import uuid
import time
import threading
import os

KAFKA_BROKER_URL = os.getenv('KAFKA_BROKER_URL', 'localhost:9092')

#KAFKA PRODUCER
try:
    client = KafkaClient(hosts=KAFKA_BROKER_URL)
    topic = client.topics['flightdata']
    producer = topic.get_sync_producer()
except Exception as e:
    print(f"Failed to connect to Kafka: {e}")
    exit()

#GENERATE UUID
def generate_uuid():
    return uuid.uuid4()

# Handle one flight in a thread
def simulate_flight_thread(geojson_file_path, airline_name, flight_number):
    try:
        with open(geojson_file_path) as f:
            json_array = json.load(f)
        coordinates = json_array['features'][0]['geometry']['coordinates']
    except FileNotFoundError:
        print(f"Error: GeoJSON file not found at {geojson_file_path} for flight {airline_name} {flight_number}")
        return
    except (KeyError, IndexError) as e:
        print(f"Error: Could not read coordinates from {geojson_file_path} for {airline_name} {flight_number}. Invalid format? {e}")
        return
    except json.JSONDecodeError as e:
        print(f"Error: Could not decode JSON from {geojson_file_path} for {airline_name} {flight_number}. {e}")
        return

    print(f"Starting flight simulation: {airline_name} {flight_number} using {geojson_file_path}")

    # Local data dictionary for this flight thread
    flight_data = {}
    flight_data['airline'] = airline_name
    flight_data['flight'] = flight_number
    
    i = 0
    while True: # Changed from while i < len(coordinates) to ensure continuous loop
        flight_data['key'] = flight_data['airline'] + '_' + str(generate_uuid())
        flight_data['timestamp'] = str(datetime.utcnow())
        flight_data['latitude'] = coordinates[i][1]
        flight_data['longitude'] = coordinates[i][0]
        message = json.dumps(flight_data)
        
        try:
            producer.produce(message.encode('ascii'))
            # print(f"Sent: {message}") # Uncomment for debugging
        except Exception as e:
            print(f"Error producing message for {airline_name} {flight_number}: {e}")
            # Consider adding a small delay or retry mechanism if Kafka is temporarily unavailable
            time.sleep(5) # Wait before trying to send next message
            continue # Continue to next iteration of the loop

        time.sleep(1)

        #if flight reaches last coordinate, start from beginning
        if i == len(coordinates)-1:
            i = 0
        else:
            i += 1

if __name__ == "__main__":
    flights = [
        ('./data/flight1.json', 'Ryanair', 'RYR50HA'),
        ('./data/flight2.json', 'Lufthansa', 'DLH1061'),
    ]

    threads = []
    for flight_config in flights:
        geojson_path, airline, flight_num = flight_config
        thread = threading.Thread(target=simulate_flight_thread, args=(geojson_path, airline, flight_num))
        threads.append(thread)
        thread.start()

    print("All flight simulation threads started.") # This prints when threads are launched

    # Keep the main thread alive while other threads run, and wait for them to complete
    # This is useful if you want the script to run until all threads are done (e.g. if they had a condition to stop)
    # For indefinitely running flights, this will also run indefinitely.
    for thread in threads:
        thread.join()
    
    print("All flight simulations have completed.") # This will only be reached if threads can complete