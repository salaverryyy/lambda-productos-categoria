import os
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
            'body': json.dumps({'message': 'Falta parámetro id en la ruta'})
        }

    # 3. Obtener ítem de DynamoDB
    try:
        response = products_table.get_item(
            Key={'id_producto': int(prod_id)}
        )
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Error al leer BD', 'error': str(e)})
        }

    item = response.get('Item')
    if not item:
        return {
            'statusCode': 404,
            'body': json.dumps({'message': 'Producto no encontrado'})
        }

    # 4. Devolver producto
    return {
        'statusCode': 200,
        'body': json.dumps(item)
    }
