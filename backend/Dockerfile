FROM python:3.11-alpine

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /app/backend

COPY requirements.txt /app/backend/

# Build psycopg2-binary from source -- add required required dependencies
RUN apk add --virtual .build-deps --no-cache postgresql-dev gcc python3-dev musl-dev
RUN apk add libffi-dev
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
RUN apk --purge del .build-deps
COPY . /app/backend/

CMD [ "/bin/sh", "-c", "python init_db.py; python manage.py migrate; python manage.py runserver 0.0.0.0:8000" ]