import os
import json
from infrastructure.dynamodb_client import products_table
from infrastructure.jwt_validator import verify_jwt, UnauthorizedError
from boto3.dynamodb.conditions import Key

def lambda_handler(event, context):
    # 1. Verificar JWT
    try:
        verify_jwt(event)
    except UnauthorizedError as e:
        return {
            'statusCode': 401,
            'body': json.dumps({'message': str(e)})
        }

    # 2. Leer parámetros de consulta para paginación
    params = event.get('queryStringParameters') or {}
    try:
        limit = int(params.get('limit', '10'))
    except ValueError:
        limit = 10
    last_key = params.get('lastKey')

    # 3. Construir argumentos de scan
    scan_kwargs = {'Limit': limit}
    if last_key:
        # lastKey debe ser un JSON string con el mapa de clave de DynamoDB
        scan_kwargs['ExclusiveStartKey'] = json.loads(last_key)

    # 4. Ejecutar scan en la tabla de productos
    response = products_table.scan(**scan_kwargs)
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
