FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py flight.py ./
COPY data/ ./data/
COPY templates/ ./templates/
COPY static/ ./static/

CMD ["python3", "app.py"]