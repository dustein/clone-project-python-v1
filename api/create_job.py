import json
from custom_encoder import CustomEncoder
import boto3
# from boto3.dynamodb.conditions import Key


dynamodbTableName = 'clone-jobs'
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(dynamodbTableName)

def lambda_handler(event, context):
    
    new_job = json.loads(event.get('body'))
    
    table.put_item(
        Item = {
          'PK': new_job['PK'],
          'SK' : new_job['SK'],
          'Data': new_job['Data'],
          'GSI1-PK': new_job['GSI1-PK'],
          'GSI1-SK': new_job['GSI1-SK'],
          'Setor': new_job['Setor'],
          'Turno': new_job['Turno'], 
        }
      )
    
    return response_builder(201, new_job)


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