import json, boto3
from botocore.vendored import requests

def lambda_handler(event, context):
    string = event['Records'][0]['body']
    x=json.loads(string)
    x=json.loads(x['Message'])

    url = 'http://<logstash ip/host>:8080'
    data = {
        'mailD': {
            'messageId': x['mail']['messageId'],
            'source': x['mail']['source'],
            'notificationType': x['notificationType'],
            'destination': x['mail']['destination'][0]
        },
        'sent-at': x['mail']['timestamp']
    }
    headers = {
        'Content-type': 'application/json',
        'Accept': 'text/plain'
    }
    r = requests.put(url, data=json.dumps(data), headers=headers)
    print(r)
