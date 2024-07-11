include ../.env.local

install:
	pip install -r requirements.txt
install-dev:
	pip install -r requirements.dev.txt
init_db:
	DB_HOST=${DB_HOST} DB_PORT=${DB_PORT} DB_NAME=${DB_NAME} DB_NAME_BACKEND=${DB_NAME_BACKEND} DB_USER=${DB_USER} DB_PASSWORD=${DB_PASSWORD} python -m init_db
lint:
	black .
test:
	pytest .