# Resistance

The Resistance is a board game (Avalon: The Resistance) built into a website for the purpose of expanding roles. The purpose of this project was to build a website capable of utilizing Django Channels and to practice deploying it to an AWS EC2 instance. The functionality of the website is not complete and was primarily meant for learning and demonstration purposes.

## How to start local server (windows):
To set up websocket, install WSL/ubuntu to run redis
    https://docs.microsoft.com/en-us/windows/wsl/install-win10
On ubuntu WSL 2, run redis on port 6379 (specified in settings.py)-
    sudo apt get redis
    sudo redis-server -p 6379
Then,
```
git clone https://github.com/sjbriley/resistance
cd resistance
python -m venv virtualenv
virtualenv/scripts/pip install -r requirements.txt
virtualenv/scripts/python manage.py collectstatic
virtualenv/scripts/python manage.py migrate --run-syncdb
echo SECRET_KEY=changeme12345 > resistance/.env
echo DEBUG=TRUE >> resistance/.env
virtualenv/scripts/python manage.py runserver 
```

for issues with migrations, try with a specific app-
    python manage.py makemigrations online
    python manage.py migrate
