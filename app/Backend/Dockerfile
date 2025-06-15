FROM python:3.13.2-slim AS builder

WORKDIR /app

COPY . . 

RUN pip install -r requirements.txt

CMD ["python", "./src/main.py"]