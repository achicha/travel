import os
from envparse import env

if os.path.isfile('.env'):
    env.read_envfile('.env')

DATABASE_URL = env.str('DATABASE_URL')
HEROKU_URL = env.str('HEROKU_URL')
URL_SUFFIX = env.str('URL_SUFFIX')
