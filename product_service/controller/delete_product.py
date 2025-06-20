import json
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

    # 2. Leer productId de pathParameters
    path = event.get('pathParameters') or {}
    prod_id = path.get('id')
    if not prod_id:
        return {
            'statusCode': 400,
            'body': json.dumps({'message': 'Falta parámetro id'})
        }

    # 3. Ejecutar delete_item en DynamoDB
    try:
        products_table.delete_item(Key={'id_producto': int(prod_id)})
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Error eliminando producto', 'error': str(e)})
        }

    # 4. Confirmación de borrado
    return {
        'statusCode': 200,
        'body': json.dumps({'message': 'Producto eliminado'})
    }
