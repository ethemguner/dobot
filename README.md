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

# Running System
If you run the server you will see nothing is happening. Because you need to
activate celery and celerybeat to get some action.

### Open two terminal, in one of them run in dobot/dobot

``export DJANGO_SETTINGS_MODULE=dobot.settings``

### and then

```celery -A dobot worker -Q price_update,celery --autoscale=2,5 -l INFO ```

### Open your other terminal and run in dobot/dobot

```export DJANGO_SETTINGS_MODULE=dobot.settings```

### and then
```celery -A dobot beat -l debug```


You good to go!



