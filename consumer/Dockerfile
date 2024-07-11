FROM python:3.11-alpine

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /app/consumer

COPY requirements.txt /app/consumer/

# Build psycopg2-binary from source -- add required required dependencies
RUN apk add --virtual .build-deps --no-cache postgresql-dev gcc python3-dev musl-dev
RUN apk add libffi-dev
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
RUN apk --purge del .build-deps
COPY . /app/consumer/