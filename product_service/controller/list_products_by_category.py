import os
import json
from boto3.dynamodb.conditions import Key
from infrastructure.dynamodb_client import products_table
from infrastructure.jwt_validator import verify_jwt, UnauthorizedError

def lambda_handler(event, context):
    # 1. Verificar JWT
    try:
        verify_jwt(event)
    except UnauthorizedError as e:
        return {
            'statusCode': 401,
            'body': json.dumps({'message': str(e)})
        }

    # 2. Leer parámetros de consulta
    params = event.get('queryStringParameters') or {}
    category_id = params.get('categoryId')
    if not category_id:
        return {
            'statusCode': 400,
            'body': json.dumps({'message': 'Falta parámetro categoryId'})
        }

    try:
        limit = int(params.get('limit', '10'))
    except ValueError:
        limit = 10

    last_key = params.get('lastKey')

    # 3. Construir argumentos de query
    query_kwargs = {
        'IndexName': 'CategoryIndex',  # GSI sobre category_id
        'KeyConditionExpression': Key('category_id').eq(category_id),
        'Limit': limit
    }
    if last_key:
        query_kwargs['ExclusiveStartKey'] = json.loads(last_key)

    # 4. Ejecutar query en DynamoDB
    response = products_table.query(**query_kwargs)
    items = response.get('Items', [])
    last_evaluated_key = response.get('LastEvaluatedKey')

    # 5. Devolver resultados y la key para la siguiente página
    body = {
        'products': items,
        'lastKey': json.dumps(last_evaluated_key) if last_evaluated_key else None
    }
    return {
        'statusCode': 200,
        'body': json.dumps(body)
    }
