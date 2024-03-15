import json
import boto3
from boto3.dynamodb.conditions import Key
from custom_encoder import CustomEncoder

dynamodbTableName = 'clone-jobs'
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(dynamodbTableName)

dynamoIndexName = 'equipe-accept-index'
index = dynamodb.Table(dynamoIndexName)

def lambda_handler(event, context):

  if event['queryStringParameters']:

    equipe = event['queryStringParameters']['GS1-PK']
    # open_jobs = event['queryStringParameters']['GS1-SK']

    response = index.query(
      KeyConditionExpression = Key ('GS1-PK').eq(equipe)
      )

    if response:
      return response_builder(200, response)
    return response_builder(404, {"message":"Equipe %" % equipe})
  
  else:
    return response_builder(404, {"message":"Informe os Parâmetros necessários para a busca."})



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