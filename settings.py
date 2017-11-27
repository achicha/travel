import os
import sys
from envparse import env

path = os.path.abspath(os.path.dirname(sys.argv[0]))

if os.path.isfile(os.path.join(path, '.env')):
    env.read_envfile(os.path.join(path, '.env'))

DATABASE_URL = env.str('DATABASE_URL')
HEROKU_URL = env.str('HEROKU_URL')
URL_SUFFIX = env.str('URL_SUFFIX')
