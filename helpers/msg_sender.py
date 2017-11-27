# send messages to remote REST API server
import json
from grab import Grab


def send(URL, msg):
    g = Grab()
    headers = {
        'Content-Type': 'application/json'
    }
    data = {'message':
                {'text': msg}
            }

    g.go(URL, headers=headers, post=json.dumps(data))
