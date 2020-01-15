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
        _DB = db.DynamoDBSchoolMembers(
            boto3.resource('dynamodb').Table(
                os.environ['APP_TABLE_NAME'])
        )
    return _DB

#top
@app.route('/', methods=['GET'])
def get_top():
    return 'wlcome to School Members APIです'

#全員参照
@app.route('/members', methods=['GET'])
def get_members():
    return str(get_app_db().list_all_items())

#一人参照
@app.route('/members/{id}', methods=['GET'])
def get_member(id):
    return str(get_app_db().get_item(id))

#追加
@app.route('/members', methods=['POST'])
def add_new_member():
    body = app.current_request.json_body
    id = get_app_db().add_item(
        subject=body.get('subject'),
        name=body.get('name'),
        mail=body.get('mail'),
        remarks=body.get('remarks'),
    )
    return str(get_member(id))

#更新
@app.route('/members/{id}', methods=['PUT'])
def update_SchoolMembers(id):
    body = app.current_request.json_body
    get_app_db().update_item(
        id,
        subject=body.get('subject'),
        name=body.get('name'),
        mail=body.get('mail'),
        remarks=body.get('remarks')
    )
    return str(get_member(id))
