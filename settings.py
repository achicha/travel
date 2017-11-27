import os
import sys
from envparse import env

if os.path.isfile('.env'):
    env.read_envfile(os.path.join(os.path.abspath(os.path.dirname(sys.argv[0])), '.env'))

DATABASE_URL = env.str('DATABASE_URL')
HEROKU_URL = env.str('HEROKU_URL')
URL_SUFFIX = env.str('URL_SUFFIX')
