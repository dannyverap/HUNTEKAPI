# API

## About

API - Huntek

Technologies used:
- [FastAPI](https://fastapi.tiangolo.com/)
- [Uvicorn](https://www.uvicorn.org/)
- [Postgres](https://www.postgresql.org/)
- [SQLAlchemy](https://docs.sqlalchemy.org/en/14/)
- [Alembic](https://alembic.sqlalchemy.org/en/latest/)

## Installation
```bash
git clone git@github.com:huntekapp/api.git
```

### Create .env file
```bash
cp .env.example .env
```

## Note for Windows users
If you are using Windows, maybe the **entrypoint.sh** use a different end of line character.
- Check the end of line character of the **entrypoint.sh** file, it should be **LF**.
- If it is not LF, change it to LF.
- In VSCode you can change it in the bottom right corner. It should say **CRLF**, click on it and change it to **LF**.

## Setup for local development option 1
If you want to run the app locally, you need to have a running Postgres database. You can use docker-compose to run the database and the app.
```
docker-compose up
```

## Setup for local development option 2
If you prefer to run the app with a different database, you can use the following commands to run the app locally.
```bash
docker compose run --rm api
```
**Note:** You need to set the environment variables in the .env file.

### Autogeneration of tables with alembic
```bash 
docker compose exec -it api bash
```
Inside the container:
```bash
alembic revision --autogenerate -m "create tables"
alembic upgrade head
```

### Populate necessary data

- To create a new set of roles:
```bash
docker compose exec api python -m src.run roles new-role
```

- To populate the plan for an enterprise:
```bash
docker compose exec api python -m src.run enterprises fill-plan
```

### Recommendations (optional)
Obtain the IP address of the docker0 (connection between the docker container and your computer) to use it in the POSTGRES_SERVER environment variable.

Copy the Wi-Fi Wireless LAN IPv4 Address:
```bash 
ipconfig
```