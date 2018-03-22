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

DESTINATIONS = [
    {
        'origin_airport': 'EVN',
        'destination_airport': 'MOW',
        'price': 5500
    },
    {
        'origin_airport': 'LWN',
        'destination_airport': 'MOW',
        'price': 5500
    }
]
