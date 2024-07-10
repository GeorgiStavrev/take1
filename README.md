# Take1
A simple implementation of an analytics service with Python (Django) and Kafka, along with an example front-end which contains a small client tracker library.

# Technology stack
- Backend (API) - handles tracking requests from clients
  - Python
  - Django
  - SQLAlchemy
  - python-kafka
- Kafka - used to stream events from the Backend application to Consumer(s)
- Consumer - processes tracking payloads and writes to DB
  - Python
  - SQLAlchemy
  - python-kafka
- Postgres - used to store events, event and user properties as well as django admin data
- Frontend - example front-end application. Contains `tracker.js` which is a simple implementation of a tracking client library
  - React

# Running
```bash
docker-compose up
```

# Developing
I suggest commenting out the `backend`, `consumer`, `frontend` components from the `docker.compose.yaml` then:
1. run `docker-compose up` to start external services
2. Start `backend` and `consumer` with the commands described in `.vscode/launch.json`
3. Start the `frontend` with `npm start`

At that point you can edit the code in `backend` and `frontend` and the apps will hot-reload. If you update the `consumer` you'll have to relaunch it.

# Future development (planned)
- Unit tests
- Move the tracker js library as a standalone project
- Easier local development
- More documentation
- IaC on AWS with Terraform
- A more suffisticated consumer application along with ability to launch many consumers at once
- Global configuration