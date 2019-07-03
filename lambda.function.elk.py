import json, boto3
from botocore.vendored import requests

def lambda_handler(event, context):
    string = event['Records'][0]['body']
    x=json.loads(string)
    x=json.loads(x['Message'])

    url = 'http://<logstash ip/host>:8080'
    headers = {
        'Content-type': 'application/json',
        'Accept': 'text/plain'
    }
    
    logstashUsername = '<logstash-username>'
    logstashPassword = '<logstash-password>'
    
    if(x['notificationType'] == 'Delivery'):
        data = {
            'mail': {
                'messageId': x['mail']['messageId'],
                'notificationType': x['notificationType'],
                'sender': x['mail']['source'],
                'recipient': x['delivery']['recipients'],
                'smtpFeedback': x['delivery']['smtpResponse']
            },
            'sent-at': x['mail']['timestamp']
        }

        r = requests.put(url, data=json.dumps(data), headers=headers, auth=(logstashUsername, logstashPassword))
        print(r)

    elif(x['notificationType'] == 'Bounce'):
        data = {
            'mail': {
                'messageId': x['mail']['messageId'],
                'notificationType': x['notificationType'],
                'sender': x['mail']['source'],
                'recipient': x['bounce']['bouncedRecipients'][0]['emailAddress'],
                'smtpFeedback': x['bounce']['bouncedRecipients'][0]['diagnosticCode']
            },
            'sent-at': x['mail']['timestamp']
        }
        r = requests.put(url, data=json.dumps(data), headers=headers, auth=(logstashUsername, logstashPassword))
        print(r)

    elif(x['notificationType'] == 'Complaint'):
        data = {
            'mail': {
                'messageId': x['mail']['messageId'],
                'notificationType': x['notificationType'],
                'sender': x['mail']['source'],
                'recipient': x['complaint']['complainedRecipients'][0]['emailAddress'],
                'smtpFeedback': x['complaint']['complaintFeedbackType']
            },
            'sent-at': x['mail']['timestamp']
        }
        
        r = requests.put(url, data=json.dumps(data), headers=headers, auth=(logstashUsername, logstashPassword))
        print(r)
        
    else:
        print('Nothing to parse')
