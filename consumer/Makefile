include ../.env

init_db:
	DB_HOST=${DB_HOST} DB_PORT=${DB_PORT} DB_NAME=${DB_NAME} DB_USER=${DB_USER} DB_PASSWORD=${DB_PASSWORD} python -m init_db
run:
	HOST=localhost PORT=9092 TOPIC=test python -m consumer.py
install:
	pip install -r requirements.txt
install-dev:
	pip install -r requirements.dev.txt
lint:
	black .
test:
	pytest .