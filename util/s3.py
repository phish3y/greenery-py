import boto3

import traceback
import json


class S3:
    def __init__(self, bucket: str, key: str):
        self.s3_client = boto3.client('s3')
        self.bucket = bucket
        self.key = key
        print('initialized s3 client')

    def get_object_from_s3(self, name: str) -> dict:
        try:
            return self.s3_client.get_object(Bucket=self.bucket,
                                             Key='{}/{}'.format(self.key, name))
        except:
            traceback.print_exc()
            return {}

    @staticmethod
    def get_content_from_s3_object(s3_object: dict) -> str:
        try:
            return str(json.loads(s3_object['Body'].read()))
        except:
            traceback.print_exc()
            return ''

    def create_s3_object(self, name: str):
        # TODO
        pass
