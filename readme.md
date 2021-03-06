# Resistance

The Resistance is a board game (Avalon: The Resistance) built into a website for the purpose of expanding roles. The purpose of this project was to build a website capable of utilizing Django Channels and to practice deploying it to an AWS EC2 instance. The functionality of the website is not complete and was primarily meant for learning and demonstration purposes.

## How to start local server (windows):

Be sure Docker & Docker-compose are installed

```
git clone https://github.com/sjbriley/resistance
cd resistance
echo SECRET_KEY=changeme12345 > resistance/.env.dev
echo DEBUG=TRUE >> resistance/.env.dev
echo HOST=redis-container >> resistance/.env.dev
docker-compose -f docker-compose.yml up -d --build
docker-compose exec web python manage.py migrate --noinput
```

or run without docker-compose

```
git clone https://github.com/sjbriley/resistance
cd resistance
echo SECRET_KEY=changeme12345 > resistance/.env
echo DEBUG=TRUE >> resistance/.env
echo HOST=localhost >> resistance/.env
docker run -p 6379:6379 --name redis-container -d redis:5
python -m venv virtualenv
virtualenv/scripts/activate
pip install -r requirements.txt
python manage.py runserver
```

Visit http://127.0.0.1:8000/

## To run in production:

```
git clone https://github.com/sjbriley/resistance
cd resistance
echo SECRET_KEY=changeme12345 > resistance/.env.prod
echo DEBUG=TRUE >> resistance/.env.prod
echo HOST=redis-container >> resistance/.env.prod

docker-compose -f docker-compose.prod.yml up -d --build
docker-compose exec web python manage.py migrate --noinput
```

To check database:

```
docker-compose exec db psql --username=hello_django --dbname=django_db_env
```

To bring down:
```
docker-compose -f docker-compose.prod.yml down -v
docker-compose -f docker-compose.yml down -v
```

for issues with migrations, try with a specific app-
    python manage.py makemigrations online
    python manage.py migrate

To backup database:

```
docker-compose -f docker-compose.prod.yml exec resistance_db_1 backup
docker exec -u sjbriley -i resistance_db_1 pg_dump -Fc db > db.dump
```

View backups:
```
docker-compose -f docker-compose.prod.yml exec resistance_db_1 backups
```