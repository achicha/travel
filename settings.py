import os
import sys
from envparse import env

path = os.path.abspath(os.path.dirname(sys.argv[0]))

if os.path.isfile(os.path.join(path, '.env')):
    env.read_envfile(os.path.join(path, '.env'))

DATABASE_URL = env.str('DATABASE_CON') + os.path.join(path, env.str('DATABASE_NAME'))
HEROKU_URL = env.str('HEROKU_URL')
TRAVEL_ROUTE = env.str('TRAVEL_ROUTE')
CHAT_ID = env.int('CHAT_ID')

# celery
BROKER_URL = env.str('BROKER_URL')                          # 'amqp://user:password@127.0.0.1:5672/myvhost'
CELERY_RESULT_BACKEND = env.str('CELERY_RESULT_BACKEND')    # 'rpc'

AIRPORT_CITY_MAP = {
    'MOW': 'Moscow',
    'SVO': 'Sheremetevo',
    'DME': 'Domodedovo',
    'LWN': 'Gyumri',
    'EVN': 'Yerevan',
    'BOJ': 'Burgas'
}
