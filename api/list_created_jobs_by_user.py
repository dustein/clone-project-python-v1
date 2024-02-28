import json
import boto3
from boto3.dynamodb.conditions import Attr
from custom_encoder import CustomEncoder

dynamodbTableName = 'clone-jobs'
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(dynamodbTableName)

def lambda_handler(event, context):

  job_creator = event['queryStringParameters']['PK']

  response = table.query(
    KeyConditionExpression = Key ('PK').eq(job_creator)
    )

  if response:
    return response_builder(200, response)
  return response_builder(404, {"message":"Found NO Jobs created by this User %" % job_creator})

def response_builder(statusCode, body=None):
  res_data = {
    'statusCode' : statusCode,
    'headers': {
      'Content-Type':'application/json',
      'Acess-Control-Allow-Origin': '*'
    }
  }
  if body:
    res_data['body'] = json.dumps(body, cls=CustomEncoder)

  return res_data