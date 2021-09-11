## Wikip Telegram Bot

#### What is required?
You will need:
- python3
- python3-pip

You can resolve python modules dependencies by:
```sh
sudo pip install -r requirements.txt
```

*Config:*
- Edit ***conf/token.conf.dist*** using your token received from BotFather 
and save it to ***conf/token.conf***

#### Run in production as user root

```sh
export FLASK_ENV=production
export FLASK_APP=app.py

nohup flask run --host=0.0.0.0 --port 80
```