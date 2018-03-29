from celery import Celery
import os

celery = Celery('tasks')
#celery = Celery('tasks', backend='rpc', broker='amqp://user:password@127.0.0.1:5672/myvhost')
celery.config_from_object('celeryconfig')
path = os.path.abspath(os.path.dirname(__file__))


@celery.task
def aviasales_gyumri():
    command = 'python ' + os.path.join(path, 'run.py') + ' aviasales -from LWN -to MOW -s 2018-04-28 -e 2018-05-03 -p 10200'
    os.system(command)
