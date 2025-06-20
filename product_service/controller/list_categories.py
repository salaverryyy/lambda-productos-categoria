import json
from infrastructure.dynamodb_client import categories_table
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

    # 2. Listar todas las categorías
    try:
        response = categories_table.scan()
        items = response.get('Items', [])
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Error leyendo categorías', 'error': str(e)})
        }

    # 3. Devolver listado
    return {
        'statusCode': 200,
        'body': json.dumps({'categories': items})
    }
