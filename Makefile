venv:
	python3.11 -m venv
activate:
	./env/bin/activate
env_export:
	sed -E -n 's/[^#]+/export &/ p' .env.local > .env.export
backend: env_export
	source .env.export && cd backend && python manage.py runserver
.PHONY: backend