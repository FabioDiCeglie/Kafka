# from pykafka import KafkaClient
# import json
# from datetime import datetime
# import uuid
# import time

# #READ COORDINATES FROM GEOJSON
# input_file = open('./data/flight1.json')
# json_array = json.load(input_file)
# coordinates = json_array['features'][0]['geometry']['coordinates']
# # print (coordinates)

# # KAFKA PRODUCER
# client = KafkaClient(hosts="localhost:9092")
# topic = client.topics['flightdata']
# producer = topic.get_sync_producer()

# # GENERATE UUID
# def generate_uuid():
#     return uuid.uuid4()

# # CONSTRUCT MESSAGE AND SEND IT TO KAFKA
# data = {}
# data['airline'] = 'Ryanair'
# data['flight'] = 'RYR50HA'

# def generate_current_location(coordinates):
#     i = 0
#     while i < len(coordinates):
#         data['key'] = data['airline'] + '_' + str(generate_uuid())
#         data['timestamp'] = str(datetime.utcnow())
#         data['latitude'] = coordinates[i][1]
#         data['longitude'] = coordinates[i][0]
#         message = json.dumps(data)
#         producer.produce(message.encode('ascii'))
#         time.sleep(1)

#         #if flight reaches the last coordinate, start from the beginning
#         if i == len(coordinates) - 1:
#             i = 0
#         else:
#             i += 1

# generate_current_location(coordinates)