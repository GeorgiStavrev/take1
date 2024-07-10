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