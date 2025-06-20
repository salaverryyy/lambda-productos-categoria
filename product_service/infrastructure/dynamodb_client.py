import os
import boto3

# Configura los nombres de tabla vía variables de entorno
PRODUCTS_TABLE   = os.environ.get('PRODUCTS_TABLE', 'Products')
CATEGORIES_TABLE = os.environ.get('CATEGORIES_TABLE', 'Categories')

dynamodb = boto3.resource('dynamodb')
products_table   = dynamodb.Table(PRODUCTS_TABLE)
categories_table = dynamodb.Table(CATEGORIES_TABLE)
