from celery import Celery
import os
import subprocess

celery = Celery('tasks')
#celery = Celery('tasks', backend='rpc', broker='amqp://user:password@127.0.0.1:5672/myvhost')
celery.config_from_object('celeryconfig')
path = os.path.abspath(os.path.dirname(__file__))


@celery.task
def aviasales_parser(from_='LWN', to='MOW',
                     start='2018-04-28', end='2018-05-03', price='10000'):

    command = 'python ' + os.path.join(path, 'run.py') + \
              ' aviasales -from {} -to {} -s {} -e {} -p {}'.format(from_, to, start, end, price)
    #r = os.system(command)
    result = subprocess.check_output(command.split(), stderr=subprocess.STDOUT)
    return result.decode()


if __name__ == '__main__':
    aviasales_parser()
