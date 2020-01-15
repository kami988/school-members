import os
import uuid
import json
import argparse

import boto3


TABLES = {
    'app': {
        'prefix': 'school-members',
        'env_var': 'APP_TABLE_NAME',
        'hash_key': 'id',
    },
}


def create_table(table_name_prefix, id):
    table_name = '%s-%s' % (table_name_prefix, str(uuid.uuid4()))
    client = boto3.client('dynamodb')
    key_schema = [
        {
            'AttributeName': id,
            'KeyType': 'HASH',
        },
    ]
    attribute_definitions = [
        {
            'AttributeName': id,
            'AttributeType': 'S',
        },
    ]
    client.create_table(
        TableName=table_name,
        KeySchema=key_schema,
        AttributeDefinitions=attribute_definitions,
        ProvisionedThroughput={
            'ReadCapacityUnits': 50,
            'WriteCapacityUnits': 50,
        }
    )
    waiter = client.get_waiter('table_exists')
    waiter.wait(TableName=table_name, WaiterConfig={'Delay': 1})
    return table_name


def record_as_env_var(key, value, stage):
    with open(os.path.join('.chalice', 'config.json')) as f:
        data = json.load(f)
        data['stages'].setdefault(stage, {}).setdefault(
            'environment_variables', {}
        )[key] = value
    with open(os.path.join('.chalice', 'config.json'), 'w') as f:
        serialized = json.dumps(data, indent=2, separators=(',', ': '))
        f.write(serialized + '\n')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--stage', default='dev')
    parser.add_argument('-t', '--table-type', default='app',
                        choices=['app'],
                        help='Specify which type to create')
    args = parser.parse_args()
    table_config = TABLES[args.table_type]
    table_name = create_table(
        table_config['prefix'], table_config['hash_key'],
    )
    record_as_env_var(table_config['env_var'], table_name, args.stage)


if __name__ == '__main__':
    main()
