import json
import boto3
# from boto3.dynamodb.conditions import Key

dynamodbTableName = 'clone-jobs'
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(dynamodbTableName)

def lambda_handler(event, context):

  user_create = 'JOB_CREATED#user_um'
  job_id = 'JOB#1'
  job_date = '2024-03-21'
  team = 'EQUIPE#4'
  accepted = 'USER_ACCEPTED#none'
  setor = 'SAP'
  turno = 'FULL'

  table.put_item(
    Item = {
      'PK': user_create,
      'SK': job_id,
      'Data': job_date,
      'GSI1-PK': team,
      'GSI1-SK': accepted,
      'Setor': setor,
      'Turno': turno
    }
  )

  response = {
    'statusCode' : 201,
    'headers': {
      'Content-Type':'application/json',
      'Acess-Control-Allow-Origin': '*'
    },
    'body': {'message': 'Job gravado'}
  }
  
  return response