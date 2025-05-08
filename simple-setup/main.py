import requests
import json
import logging
import time
from quixstreams import Application

def get_weather_data():
    response = requests.get("https://api.open-meteo.com/v1/forecast", params={
        "latitude": 51.5,
        "longitude": -0.11,
        "current": "temperature_2m",
    })
    weather = response.json()

    if weather.get("error"):
        raise Exception(f"Error fetching weather data: {weather['error']}")

    if weather.get("current", {}) is None:
        raise Exception("No weather data found")

    return weather

def main():
    app = Application(broker_address="localhost:9092", loglevel="DEBUG")

    with app.get_producer() as producer:
        weather = get_weather_data()
        logging.debug(f"Got weather: {weather}")
        producer.produce(
            topic="weather_data_demo",
            key="London",
            value=json.dumps(weather),
            )
        logging.info(f"Produced. Sleeping...")
        time.sleep(10)

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    main()
