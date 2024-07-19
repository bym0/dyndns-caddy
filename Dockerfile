# Use the official Python image as the base image
FROM python:3.9.19-slim

WORKDIR /app
COPY . .
RUN chmod +x src/main.py
CMD ["python3", "src/main.py"]
