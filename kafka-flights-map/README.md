# Kafka Flights Map

This project demonstrates a real-time flight tracking simulation using Apache Kafka and a Flask web application. A Python script produces mock flight data to a Kafka topic, and a Flask web application consumes this data to display flight positions on a map (assumption based on project name, `static/`, and `templates/` directories).

## Architecture

The system consists of the following components, orchestrated using Docker Compose:

1.  **Zookeeper (`zookeeper` service):**
    *   Manages Kafka brokers and topic metadata.
    *   Image: `confluentinc/cp-zookeeper:latest`

2.  **Kafka Broker (`kafka` service):**
    *   Message broker that receives flight data from the producer and serves it to the consumer.
    *   Image: `confluentinc/cp-kafka:latest`
    *   Advertised for internal Docker network communication (e.g., `PLAINTEXT://kafka:29092`).
    *   Advertised for host access (e.g., `PLAINTEXT_HOST://localhost:9092`).
        (Actual ports depend on environment variables set for `docker-compose`)

3.  **Flight Data Producer (`flight-producer` service):**
    *   A Python script (`flight.py`) that reads flight coordinates from JSON files (in the `data/` directory).
    *   Simulates flight movements by periodically sending updated coordinates to the `flightdata` Kafka topic.
    *   Uses `pykafka` library.

4.  **Flight Display Application (`flight-app` service):**
    *   A Flask web application (`app.py`) that consumes flight data from the `flightdata` Kafka topic.
    *   (Presumably) displays the flight locations on a map using HTML templates from the `templates/` directory and static assets from `static/`.
    *   Exposes port `5001` for web access.
    *   Uses `flask` and `pykafka` libraries.

All services run in Docker containers and are connected via a custom Docker network named `kafka-network`.

## Features

*   Real-time data streaming with Kafka.
*   Mock flight data generation.
*   Web-based visualization of flight data (presumed).
*   Containerized deployment using Docker and Docker Compose.

## Prerequisites

*   Docker
*   Docker Compose

## Project Structure

```
kafka-flights-map/
├── docker-compose.yml      # Defines and configures all services
├── Dockerfile              # Defines the Docker image for Python applications
├── flight.py               # Kafka producer script for flight data
├── app.py                  # Flask web application (Kafka consumer and UI)
├── requirements.txt        # Python dependencies
├── data/                   # Contains JSON files with flight coordinates (e.g., flight1.json, flight2.json)
├── templates/              # HTML templates for the Flask web application
├── static/                 # Static assets (CSS, JS, images) for the Flask web application
└── .env                    # (Recommended) For storing environment variable configurations
```

## Setup and Running

1.  **Clone the repository (if applicable).**

2.  **Environment Configuration:**
    It's recommended to create a `.env` file in the project root to configure the Kafka advertised listeners and other environment variables referenced in `docker-compose.yml`. Example `.env` file:
    ```env
    # For Kafka Broker (kafka service)
    KAFKA_INTERNAL_ADVERTISED_HOSTNAME=kafka
    KAFKA_INTERNAL_ADVERTISED_PORT=29092
    KAFKA_EXTERNAL_ADVERTISED_HOSTNAME=localhost
    KAFKA_EXTERNAL_ADVERTISED_PORT=9092

    # For Python Applications (flight-producer and flight-app services)
    # This should match the internal advertised listener of Kafka
    KAFKA_BROKER_URL=kafka:29092
    FLASK_DEBUG=1
    ```
    Adjust `KAFKA_EXTERNAL_ADVERTISED_HOSTNAME` if `localhost` is not appropriate for your Docker host setup.

3.  **Build and Start Services:**
    Open a terminal in the project root directory and run:
    ```bash
    docker-compose up -d
    ```
    This will build the Docker image for the Python applications and start all defined services. The `--build` flag ensures the image is rebuilt if there are changes.

4.  **Accessing the Application:**
    *   The **Flight Display Application** should be accessible at `http://localhost:5001` (or the port mapped in `docker-compose.yml` for the `flight-app` service if changed).
    *   The **Flight Producer** will start sending data to Kafka automatically.

5.  **Stopping the Services:**
    Press `Ctrl+C` in the terminal where `docker-compose up` is running, or run:
    ```bash
    docker-compose down
    ```
    This will stop and remove the containers.

## Configuration Details

*   **Kafka Broker URL (`KAFKA_BROKER_URL`):**
    *   Used by `flight.py` and `app.py` to connect to Kafka.
    *   Crucially, this URL must point to the Kafka listener advertised for *internal* communication within the Docker network (e.g., `kafka:29092` if using the example `.env` settings).

*   **Kafka Advertised Listeners:**
    *   The `kafka` service in `docker-compose.yml` uses environment variables (e.g., `KAFKA_INTERNAL_ADVERTISED_HOSTNAME`, `KAFKA_EXTERNAL_ADVERTISED_HOSTNAME`) to configure how Kafka announces itself.
    *   `PLAINTEXT://${KAFKA_INTERNAL_ADVERTISED_HOSTNAME}:${KAFKA_INTERNAL_ADVERTISED_PORT}` is for communication between containers on the same Docker network.
    *   `PLAINTEXT_HOST://${KAFKA_EXTERNAL_ADVERTISED_HOSTNAME}:${KAFKA_EXTERNAL_ADVERTISED_PORT}` is for communication from the host machine to Kafka.

## How it Works

1.  The `flight-producer` service runs `flight.py`. This script reads predefined flight paths from JSON files in the `./data/` directory.
2.  It then periodically sends messages containing flight details (airline, flight ID, timestamp, latitude, longitude) to the `flightdata` topic in the Kafka broker.
3.  The `flight-app` service runs `app.py`, a Flask application. This application acts as a Kafka consumer, subscribing to the `flightdata` topic.
4.  As new messages arrive, the Flask application processes them (presumably updating flight positions) and serves a web page (likely using `index.html` from `templates/`) that visualizes these positions, potentially on a map using JavaScript from `static/`.
