import logging
import os
import boto3

import string
import random

s3 = boto3.client('s3')


class Image:
    ALLOWED_MIMES = ['image/jpeg', 'image/png', 'image/jpg']
    BUCKET_NAME = os.environ['BUCKET_UPLOAD_IMAGES']
    EXPIRATION_TIME = 5 * 60
    errors = []

    def __init__(self, body) -> None:

        self.name = body['name'] if 'name' in body else None
        self.mime = body['mime'] if 'mime' in body else None

    def validate_mime_types(self):
        if self.mime not in self.ALLOWED_MIMES:
            logging.error('Incorrect mime type')
            self.errors.append("Mime type is not allowed")

    def validate_data(self):
        if not self.name or not self.mime:
            logging.error('There is no image in request')
            self.errors.append("Couldn't fetch image from the body")

    def validate(self):
        self.validate_data()
        self.validate_mime_types()

    def generate_path(self):
        rand = ''.join(random.choices(
            string.ascii_uppercase + string.digits, k=8))
        random_str = str(rand) + "_"
        image_path = "products/" + random_str + self.name
        return image_path

    def put_image_s3(self):
        params = {
            "Bucket": self.BUCKET_NAME,
            "Key": self.generate_path(),
            "ACL": 'public-read',
            "ContentType": self.mime
        }
        url = s3.generate_presigned_url(
            "put_object", Params=params, ExpiresIn=self.EXPIRATION_TIME
        )
        return url

    def delete_image_s3(self):
        key = 'products/' + self.name
        s3.delete_object(Bucket=self.BUCKET_NAME, Key=key)
