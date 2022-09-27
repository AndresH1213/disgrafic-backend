import os
from datetime import datetime

from pynamodb.attributes import UnicodeAttribute, NumberAttribute, UTCDateTimeAttribute
from pynamodb.indexes import GlobalSecondaryIndex, AllProjection
from pynamodb.models import Model

from jsonschema import Draft7Validator
from json import load

TABLE_NAME = os.environ['DYNAMODB_TABLE_PRODUCT']
REGION = os.environ['REGION']


class LabelIndex(GlobalSecondaryIndex):
    """
    This class represents a global secondary index
    """
    class Meta:
        index_name = 'product_label_GSI'
        read_capacity_units = 2
        write_capacity_units = 1
        # All attributes are projected
        projection = AllProjection()

    label = UnicodeAttribute(default="material", hash_key=True)
    createdAt = UTCDateTimeAttribute(
        null=False, default=datetime.now(), range_key=True)


class ProductModel(Model):
    class Meta:
        table_name = TABLE_NAME
        if 'ENV' in os.environ:
            host = 'http://localhost:8000'
        else:
            region = REGION
            host = f'https://dynamodb.{REGION}.amazonaws.com'

    product_id = UnicodeAttribute(hash_key=True, null=False)
    label = UnicodeAttribute(null=True)
    name = UnicodeAttribute(null=False)
    price = NumberAttribute(null=False)
    product_type = UnicodeAttribute(null=False)
    subtype = UnicodeAttribute(null=False)
    image_url = UnicodeAttribute(null=True)
    createdAt = UTCDateTimeAttribute(null=False, default=datetime.now())
    updatedAt = UTCDateTimeAttribute(null=False)

    # GSI declaration
    label_index = LabelIndex()

    @staticmethod
    def isValid(body):
        with open('./lib/schemas/product.json') as file:
            schema = load(file)

        validator = Draft7Validator(schema)
        schema_errors = list(validator.iter_errors(body))
        return len(schema_errors) == 0

    @staticmethod
    def has_product_changed(data, found_product):
        can_change = ['name', 'price', 'product_type', 'subtype', 'image_url']
        product_changed = False
        for field in can_change:
            if field in data and data[field] != getattr(found_product, field):
                setattr(found_product, field, data[field])
                product_changed = True

        return [product_changed, found_product]

    def save(self, conditional_operator=None, **expected_values):
        self.updatedAt = datetime.now()
        super(ProductModel, self).save()

    def __iter__(self):
        for name, attr in self.get_attributes().items():
            yield name, attr.serialize(getattr(self, name))
