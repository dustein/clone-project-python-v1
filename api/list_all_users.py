import json
import boto3
from boto3.dynamodb.conditions import Attr
from custom_encoder import CustomEncoder

dynamodbTableName = 'clone-jobs'
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(dynamodbTableName)

def lambda_handler(event, context):

  data = table.scan(FilterExpression=Attr('PK').begins_with('USER#'))
  res_data = data['Items']

  while 'LastEvaluatedKey' in data:
    data = table.scan(ExclusiveStartKey=data['LastEvaluatedKey'])
    res_data.extend(data['Items'])

  response = response_builder(200, res_data)  
  
  return response

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