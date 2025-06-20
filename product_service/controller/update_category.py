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

    # 3. Parsear body y preparar actualización
    body = json.loads(event.get('body') or '{}')
    allowed = ['nombre', 'descripcion']
    expr = []
    names  = {}
    values = {}
    for field in allowed:
        if field in body:
            expr.append(f"#{field} = :{field}")
            names[f"#{field}"]  = field
            values[f":{field}"] = body[field]

    if not expr:
        return {
            'statusCode': 400,
            'body': json.dumps({'message': 'No hay campos para actualizar'})
        }

    update_expr = "SET " + ", ".join(expr)

    # 4. Ejecutar update
    try:
        resp = categories_table.update_item(
            Key={'id_categoria': int(cat_id)},
            UpdateExpression=update_expr,
            ExpressionAttributeNames=names,
            ExpressionAttributeValues=values,
            ReturnValues='ALL_NEW'
        )
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Error modificando categoría', 'error': str(e)})
        }

    updated = resp.get('Attributes', {})
    return {
        'statusCode': 200,
        'body': json.dumps(updated)
    }
