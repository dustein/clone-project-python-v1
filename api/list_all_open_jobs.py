import json
import boto3
from boto3.dynamodb.conditions import Key
from api.custom_encoder import CustomEncoder

dynamodbTableName = 'clone-jobs'
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(dynamodbTableName)

def lambda_handler(event, context):

  if event['queryStringParameters']:

    all_jobs = []

    for num in range (1,5):
      equipe = f'EQUIPE#{num}'
      
      equipe_job = table.query(
      IndexName = 'equipe-accept-index',
      KeyConditionExpression = Key (equipe).eq(equipe) & Key ('GSI1-SK').begins_with('USER_ACCEPTED#')
      )

      all_jobs.append(equipe_job)

    response = all_jobs
    
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