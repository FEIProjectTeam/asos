# Photo gallery

## Prerequisites
Make sure the following tools are installed on your system:

- Docker
- Docker Compose

## Build and run Docker
### Start the Containers
```bash
docker-compose up
```
Application is running on `localhost:8000`

### Stop the Containers
Stops and remove containers
```bash
docker-compose down
```

### Rebuild Containers
If you make changes to the Dockerfile or dependencies:
```bash
docker-compose up --build
```

### Pause and start again (no changes applied)
```bash
docker-compose stop
docker-compose start
```

## Run Management Commands
You can run any Django management command inside the web container. For example:

```bash
docker-compose exec web python manage.py makemigrations
docker-compose exec web python manage.py migrate
```
