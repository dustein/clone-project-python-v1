import json
from custom_encoder import CustomEncoder
import boto3
# from boto3.dynamodb.conditions import Key


dynamodbTableName = 'clone-jobs'
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(dynamodbTableName)

def lambda_handler(event, context):
    
    new_user = json.loads(event.get('body'))
    
    table.put_item(
        Item = {
          'PK': new_user['PK'],
          'SK' : new_user['SK'],
          'E-mail': new_user['E-mail'],
          'Fone' : new_user['Fone'],
          'Funcional' : new_user['Funcional'],
          'GSI1-PK': new_user['GSI1-PK'],
          'GSI1-SK': new_user['GSI1-SK'],
          'Nome' : new_user['Nome'] 
        }
      )
    
    return response_builder(201, new_user)


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

# Modelo Body
# {
#   "PK": "USER#teste1",
#   "SK" : "USER#teste1",
#   "E-mail": "teste@email.com",
#   "Fone" : 11111,
#   "Funcional" : 11111,
#   "GSI1-PK": "EQUIPE#1",
#   "GSI1-SK": "SETOR#SAP",
#   "Nome" : "Ususario Teste 1"
# }