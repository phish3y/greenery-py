import boto3

import traceback

from util.logger import Logger


class S3:
    def __init__(self, bucket: str, key: str):
        self.s3_client = boto3.client('s3')
        self.bucket = bucket
        self.key = key
        self.logger = Logger()
        self.logger.log_info('initialized s3 client')

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
            return s3_object['Body'].read().decode('utf-8')
        except:
            traceback.print_exc()
            return ''

    def create_s3_object(self, greenery_id: str, json_body: str):
        try:
            self.s3_client.put_object(Bucket=self.bucket,
                                      Key='{}/{}'.format(self.key, greenery_id),
                                      Body=json_body.encode('utf-8'))
            return True
        except:
            traceback.print_exc()
            return False
