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

    # 2. Parsear body
    body = json.loads(event.get('body') or '{}')
    required = ['id_categoria', 'nombre', 'descripcion']
    if not all(k in body for k in required):
        return {
            'statusCode': 400,
            'body': json.dumps({'message': f'Faltan campos: {required}'})
        }

    item = {
        'id_categoria': int(body['id_categoria']),
        'nombre': body['nombre'],
        'descripcion': body['descripcion']
    }

    # 3. Insertar en DynamoDB
    try:
        categories_table.put_item(Item=item)
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Error creando categoría', 'error': str(e)})
        }

    # 4. Confirmación
    return {
        'statusCode': 201,
        'body': json.dumps(item)
    }
