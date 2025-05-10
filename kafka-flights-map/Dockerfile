FROM python:3.9-slim

WORKDIR /app

RUN pip install uv

COPY requirements.txt requirements.txt
RUN uv pip install --no-cache-dir -r requirements.txt

COPY app.py flight.py index.html data/ static/ ./

CMD ["uv", "run", "app.py"]