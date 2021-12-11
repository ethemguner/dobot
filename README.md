# Django Setup
* Create your environment. Python 3.6.5 & 3.8.10 is fine.
* Install requirements.txt to the environment. (If you're using 3.8 python you 
may see some errors, but not critical ones)
* Install postgre-12, create db with creds:
  * db name: dobotdb
  * user: dobot
  * password: safa0606
* Makemigrations & migrate.

# Redis
* Straightforward install, nothing complicated.

# RabbitMQ
* Straightforward install, nothing complicated.
* Don't forget to install rabbitmq plugin to browse ui.

# Running System Over Binance Websocket (Recommended)
* Open a new terminal
* Go to project path.
* Activate your environment.
* Run ```python3 binance_websocket_listener.py```

You may encounter binance API errors because requests are restricted. 
Only produ

# Running System Over Celery Service
Because we're sending processes to query, you may encounter delays in price
changes. Also there is a 2.35 seconds delay in code, otherwise binance is
throwing connection timeout error. This is why using binance websocket listener
is recommended.

### Open two terminal, in one of them run in dobot/dobot

./ssc/celery.sh

### Open your other terminal and run in dobot/dobot

./ssc/celerybeat.sh


You good to go!



