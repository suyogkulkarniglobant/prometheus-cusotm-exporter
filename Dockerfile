FROM --platform=linux/amd64 python:3.8-slim-buster as build

WORKDIR /app
RUN pip3 install prometheus_client
COPY custom_exporter.py .
CMD ["python3", "custom_exporter.py" , "--folder", "/bin"]
