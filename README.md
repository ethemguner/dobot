# Dobot
Dobot is a crypto currency trade bot by made [Dopigo](https://github.com/Dopigo) 
developer members.

## Before Installation
You need .localsecrets file to run the project and other executions. Please contact
with [Ethem](https://github.com/ethemguner) or [Sencer H.](https://github.com/RecNes)
before you start install the project.

## If You Gott .localsecrets File
* Place it out of the project.
* Execute commands accordingly:
  * `set -a`
  * `source /path/to/.localsecrets`
  * `set +a`

From now on, you will be able to run migrations & binance websocket listener.

## Django Setup
* Create your environment. Python 3.7+ version required.
* Install requirements.txt to the environment. (If you're using 3.8 python you 
may see some errors, but not critical ones)
* Install postgre-12, create db with creds:
  * db name: dobotdb
  * user: dobot
  * password: safa0606
* Makemigrations & migrate.

## Redis
* Straightforward install, nothing complicated.

## RabbitMQ
* Straightforward install, nothing complicated.
* Don't forget to install rabbitmq plugin to browse ui.

## Running System Over Binance Websocket (Recommended)
* Open a new terminal
* Activate your environment
* Go to project root (where manage.py is living).
* Run ```python3 binance_websocket_listener.py```

You may encounter binance API errors because requests are IP based restricted. If so,
please contact with [Ethem](https://github.com/ethemguner).

## Running System Over Celery Service (not essential right now)
Because we're sending processes to query, you may encounter delays in price
changes. Also there is a 2.35 seconds delay in code, otherwise binance is
throwing connection timeout error. This is why using binance websocket listener
is recommended. **Currently, this is not a necessarry part of the project.**

### Open two terminal, in one of them run in dobot/dobot

./ssc/celery.sh

### Open your other terminal and run in dobot/dobot

./ssc/celerybeat.sh


You good to go!



