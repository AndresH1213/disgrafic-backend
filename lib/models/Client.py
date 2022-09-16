import os
from datetime import datetime

from pynamodb.attributes import UnicodeAttribute, UTCDateTimeAttribute
from pynamodb.models import Model

from jsonschema import Draft7Validator
from json import load

TABLE_NAME = os.environ['DYNAMODB_TABLE_CLIENT']
REGION = os.environ['REGION']


class ClientModel(Model):
    class Meta:
        table_name = TABLE_NAME
        if 'ENV' in os.environ:
            host = 'http://localhost:8000'
        else:
            region = REGION
            host = f'https://dynamodb.{REGION}.amazonaws.com'

    client_id = UnicodeAttribute(hash_key=True, null=False)
    name = UnicodeAttribute(null=False)
    email = UnicodeAttribute(null=False)
    phone = UnicodeAttribute()
    address = UnicodeAttribute()
    createdAt = UTCDateTimeAttribute(null=False, default=datetime.now())

    @staticmethod
    def isValid(body):
        with open('./lib/schemas/client.json') as file:
            schema = load(file)

        validator = Draft7Validator(schema)
        schema_errors = list(validator.iter_errors(body))
        return len(schema_errors) == 0

    def save(self, conditional_operator=None, **expected_values):
        self.updatedAt = datetime.now()
        super(ClientModel, self).save()

    def __iter__(self):
        for name, attr in self._get_attributes().items():
            yield name, attr.serialize(getattr(self, name))
