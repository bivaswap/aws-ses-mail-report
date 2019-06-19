#from __future__ import print_function
#import os
import json
import boto3

def lambda_handler(event, context):
    # Handling data from SNS
    # string = event['Records'][0]['Sns']['Message']
    # x=json.loads(string)
    # print(x['notificationType'])
    
    # Handling data from SQS
    string = event['Records'][0]['body']
    x=json.loads(string)
    x=json.loads(x['Message'])
    
    dynamodb = boto3.resource('dynamodb')
    dynamoTable = dynamodb.Table('Mail_Report')
    dynamoTable.put_item(
        Item={
            'messageId': x['mail']['messageId'],
            'source': x['mail']['source'],
            'notificationType': x['notificationType'],
            'destination': x['mail']['destination'][0],
            'timestamp': x['mail']['timestamp']
        }
        )
