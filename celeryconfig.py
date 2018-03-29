from celery.schedules import crontab
from settings import BROKER_URL, CELERY_RESULT_BACKEND


CELERYBEAT_SCHEDULE = {
    'every-hour': {
        'task': 'tasks.aviasales_gyumri',
        'schedule': crontab(minute='*/3'), # (minute=0, hour='8-22'),
        #'args': 'aviasales -from LWN -to MOW -s 2018-04-28 -e 2018-05-03 -p 10200'
    },
}
