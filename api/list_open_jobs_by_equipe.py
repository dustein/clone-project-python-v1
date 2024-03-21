import json
import boto3
from boto3.dynamodb.conditions import Key
from api.custom_encoder import CustomEncoder

dynamodbTableName = 'clone-jobs'
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(dynamodbTableName)

def lambda_handler(event, context):

  if event['queryStringParameters']:

    equipe = event['queryStringParameters']['GSI1-PK']

    response = table.query(
      IndexName = 'equipe-accept-index',
      KeyConditionExpression = Key ('GSI1-PK').eq(equipe) & Key ('GSI1-SK').begins_with('USER_ACCEPTED#')
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