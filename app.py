from chalice import Chalice
from chalice import Response
from chalicelib import db
import os
import boto3

app = Chalice(app_name='school-members')
app.debug = True
_DB = None


def get_app_db():
    global _DB
    if _DB is None:
        _DB = db.DynamoDBTodo(
            boto3.resource('dynamodb').Table(
                os.environ['APP_TABLE_NAME'])
        )
    return _DB

#全員参照
@app.route('/', methods=['GET'])
def get_members():
    return get_app_db().list_all_items()

#一人参照
@app.route('/{id}', methods=['GET'])
def get_member(id):
    return get_app_db().get_item(id)

#追加
@app.route('/', methods=['POST'])
def add_new_member():
    body = app.current_request.json_body
    return get_app_db().add_item(
        subject=body.get('subject'),
        name=body.get('name'),
        mail=body.get('mail'),
        remarks=body.get('remarks'),
    )

#更新
@app.route('/{id}', methods=['PUT'])
def update_todo(id):
    body = app.current_request.json_body
    return get_app_db().update_item(
        id,
        subject=body.get('subject'),
        name=body.get('name'),
        mail=body.get('mail'),
        remarks=body.get('remarks')
    )
