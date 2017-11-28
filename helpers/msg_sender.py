# send messages to remote REST API server
import json
#from grab import Grab
import requests


def send(URL, msg):
    #g = Grab()
    headers = {
        'Content-Type': 'application/json'
    }
    data = {'message':
                {'text': msg}
            }

    requests.post(URL, headers=headers, data=json.dumps(data))
    #g.go(URL, headers=headers, post=json.dumps(data))
