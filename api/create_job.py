import json
import boto3
from boto3.dynamodb.conditions import Key
from custom_encoder import CustomEncoder

dynamodbTableName = 'clone-jobs'
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(dynamodbTableName)

def lambda_handler(event, context):

  if event['queryStringParameters']:

    user_create = 'JOB_CREATED#user_um'
    job_id = 'JOB#1'
    job_date = '2024-03-21'
    team = 'EQUIPE#4'
    accepted = 'USER_ACCEPTED#none'
    setor = 'SAP'
    turno = 'FULL'

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