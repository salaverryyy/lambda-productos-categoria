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

    # 2. Leer id de pathParameters
    path = event.get('pathParameters') or {}
    cat_id = path.get('id')
    if not cat_id:
        return {
            'statusCode': 400,
            'body': json.dumps({'message': 'Falta parámetro id'})
        }

    # 3. Eliminar de DynamoDB
    try:
        categories_table.delete_item(Key={'id_categoria': int(cat_id)})
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Error eliminando categoría', 'error': str(e)})
        }

    # 4. Confirmación
    return {
        'statusCode': 200,
        'body': json.dumps({'message': 'Categoría eliminada'})
    }
