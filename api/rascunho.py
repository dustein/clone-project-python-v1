import boto3
import json
import logging
from custom_encoder import CustomEncoder

logger = logging.getLogger()
logger.setLevel(logging.INFO)
#DynamoDB
dynamodbTableName = 'clone-jobs'
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(dynamodbTableName)
# metodos
getMethod = 'GET'
postMethod = 'POST'
patchMethod = 'PATCH'
deleteMethod = 'DELETE'
# Os paths da API
inicialPath = '/inicial'
jobsPath = '/jobs'

def lambda_handler(event, context):
  logger.info(event)
  httpMethod = event["requestContext"]["http"]["method"]
  path = event["requestContext"]["http"]["path"]

  if httpMethod == getMethod and path == inicialPath:
    response = buildResponse(200)

  elif httpMethod == getMethod and path == jobsPath:
    response = getAllJobs(event['queryStringParameters']['jobID'])
  
  elif httpMethod == postMethod and path == jobsPath:
    response = createJob(json.loads(event['body']))
  
  elif httpMethod == deleteMethod and path == jobsPath:
    requestBody = json.loads(event['body'])
    response = modifyJob(requestBody['jobID'], requestBody['updateKey'], requestBody['updateValue'])
  
  elif httpMethod == deleteMethod and path == jobsPath:
    requestBody = json.loads(event['body'])
    response = deleteJob(requestBody['jobID'])
  
  else:
    response = buildResponse(404, 'Not Found!')
  
  return response

# açoes 
def getJobById(jobID): 
  try:
    response = table.get_item(
      Key = {'jobID': jobID}
    )
    if 'Item' in response:
      return buildResponse(200, response['Item'])
    return buildResponse(404, {"message":"jobID %s not found" % jobID})
  except:
    logger.exception("A busca pelo Job não apresentou resultado!")

def getAllJobs():
  try:
    response = table.scan()
    result = response['Items']
    # este while é para caso a tabela seja muito grande pode haver erro de evauated key, então pegamos de onde parou e apensamos (estendemos) juntando tudo para ter o resultado final.
    while 'LastEvaluatedKey' in response:
      response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
      result.extend(response['Items'])
    
    body = {
      'products': result
    }

    return buildResponse(200, body)
  
  except:
    logger.exception("A busca não apresentou resultados...")

def createJob(requestBody):
  try:

    table.put_item(Item=requestBody)

    body = {
      "Operation": "SAVE",
      "Message": "Sucess",
      "Item": requestBody
    }
    return buildResponse(200, body)
  
  except:
    logger.exception("Não foi possível a criação do job.")

def modifyJob(jobID, updateKey, updateValue):
  try:
    response = table.update_item(
      Key = {
        'jobID': jobID
      },
      UpdateExpression = 'set %s = :value' % updateKey,
      ExpressionAttributeValues = {
        ':value': updateValue
      },
      ReturnValues = 'UPDATED_NEW'
    )

    body = {
      "Operation":"UPDATE",
      "Message":"SUCCESS",
      "UpdatedAttributes": response
    }

    return buildResponse(200, body)

  except:
    logger.exception("Não foi possível a modificação.")

def deleteJob(jobID):
  try:
    response = table.delete_item(
      Key = {
        'jobID': jobID
      },
      ReturnValues = 'ALL_OLD'
    )

    body = {
      "Operation": "DELETE",
      "Message": "SUCCESS",
      "deletedItem": response
    }
    return buildResponse(200, body)
  
  except:
    logger.exception("Não foi possível deletar.")


def buildResponse(statusCode, body=None):
  response = {
    'statusCode': statusCode,
    'headers': {
      'Content-Type':'application/json',
      'Acess-Control-Allow-Origin': '*' #para acessar a API em hospedagem de fora CORS
    }
  }
  if body is not None:
    response['body'] = json.dumps(body, cls=CustomEncoder)