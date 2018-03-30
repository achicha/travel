from celery.schedules import crontab
from settings import BROKER_URL, CELERY_RESULT_BACKEND


CELERYBEAT_SCHEDULE = {
    'aviasales_gyumri': {
        'task': 'tasks.aviasales_parser',
        'schedule': crontab(minute='*/15'),  # hour='8-22'),  # every 15 minute in working hours
        'args': ('LWN', 'MOW', '2018-04-28', '2018-05-03', '4000')
    },
    'aviobilet_burgas': {
        'task': 'tasks.aviobilet_parser',
        'schedule': crontab(minute='*/15'),  # every 15 minute in working hours
        'args': ('MOW', 'BOJ', '2018-04-28', '2018-05-03', '2000')
    }


}
