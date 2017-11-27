import os
import sys
from envparse import env

path = os.path.abspath(os.path.dirname(sys.argv[0]))

if os.path.isfile(os.path.join(path, '.env')):
    env.read_envfile(os.path.join(path, '.env'))

DATABASE_URL = env.str('DATABASE_CON') + os.path.join(path, env.str('DATABASE_NAME'))
HEROKU_URL = env.str('HEROKU_URL')
URL_SUFFIX = env.str('URL_SUFFIX')
