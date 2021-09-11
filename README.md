## Wikip Web

#### What is required?
You will need:
- python3
- python3-pip

You can resolve python modules dependencies by:
```sh
sudo pip install -r requirements.txt
```


#### Run in production as user root

```sh
export FLASK_ENV=production
export FLASK_APP=app.py

nohup flask run --host=0.0.0.0 --port 80
```