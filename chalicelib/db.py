from uuid import uuid4

from boto3.dynamodb.conditions import Key


class SchoolMembersDB(object):
    def list_all_items(self):
        pass

    def get_item(self, id):
        pass

    def add_item(self, subject, name, mail=None, remarks=None):
        pass

    def update_item(self, id, subject=None, name=None, mail=None, remarks=None):
        pass

class DynamoDBSchoolMembers(SchoolMembersDB):
    def __init__(self, table_resource):
        self._table = table_resource

    def list_all_items(self):
        response = self._table.scan()
        return response['Items']

    def get_item(self, id):
        response = self._table.get_item(
            Key={
                'id': id,
            },
        )
        return response['Item']

    def add_item(self, subject, name, mail=None, remarks=None):
        id = str(uuid4())
        self._table.put_item(
            Item={
                'subject': subject,
                'name': name,
                'mail': mail if mail is not None else {},
                'remarks': remarks if remarks is not None else {},
                'id':  id,
            }
        )
        return id

    def update_item(self, id, subject=None, name=None, mail=None, remarks=None):
        # We could also use update_item() with an UpdateExpression.
        item = self.get_item(id)
        if subject is not None:
            item['subject'] = subject
        if mail is not None:
            item['mail'] = mail
        if name is not None:
            item['name'] = name
        if remarks is not None:
            item['remarks'] = remarks
        self._table.put_item(Item=item)
        return id
