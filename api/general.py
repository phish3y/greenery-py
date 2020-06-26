from pyramid.response import Response
from pyramid.request import Request

import traceback
from datetime import datetime

from util.http import build_success_response, build_error_response, get_json_body_from_request
from util.s3 import S3


class General:

    def __init__(self):
        self.s3 = S3('greenery-data', 'general')
        self.required_general_json_keys = ['name', 'phone', 'email', 'address']

    # /readGeneral
    def read_general(self, request: Request) -> Response:
        start = datetime.now()
        print(request)
        if request.method != "POST":
            return build_error_response(400, '/readGeneral requires POST http method')

        print('Beginning /readGeneral endpoint processing')
        json_body = get_json_body_from_request(request)
        if len(json_body) < 1:
            return build_error_response(400, 'Request body is not valid JSON!')
        print('parsed request body successfully')

        name = self.__get_name_from_json_body(json_body)
        if len(name) < 1:
            return build_error_response(400, "Request body must contain a populated 'name' field")
        print('extracted name {} from request body successfully'.format(name))

        s3_object: dict = self.s3.get_object_from_s3(name)
        if len(s3_object) < 1:
            return build_error_response(404, 'Failed to find {} in data store'.format(name))
        print('found general object {} in data store'.format(name))

        s3_content: str = self.s3.get_content_from_s3_object(s3_object)
        if len(s3_content) < 1:
            return build_error_response(500, 'Failed to read content from data store for {}'.format(name))
        print('read data from {} successfully'.format(name))

        response = build_success_response(s3_content)

        print('Finished successfully. Took: {}'.format(datetime.now() - start))
        return response

    # /createGeneral
    def create_general(self, request: Request) -> Response:
        start = datetime.now()
        print(request)
        if request.method != "POST":
            return build_error_response(400, '/createGeneral requires POST http method')
        print('Beginning /createGeneral endpoint processing')

        json_body: dict = get_json_body_from_request(request)
        if len(json_body) < 1:
            return build_error_response(400, 'Request body is not valid JSON!')
        print('parsed request body successfully')

        validation_errors: str = self.__validate_create_general_body(json_body)
        if len(validation_errors) > 0:
            print(validation_errors)
            return build_error_response(400, validation_errors)
        print('validated request body')

        self.s3.create_s3_object('')

        print('Finished successfully. Took: {}'.format(datetime.now() - start))
        return Response(status=200, body='wip')

    @staticmethod
    def __get_name_from_json_body(json_body: dict) -> str:
        try:
            return json_body['name']
        except:
            traceback.print_exc()
            return ''

    def __validate_create_general_body(self, json_body: dict) -> str:
        validation_errors = ''
        for required_key in self.required_general_json_keys:
            if required_key not in json_body.keys():
                validation_errors += '{} is a required key in request body;'.format(required_key)

        if validation_errors.endswith(';'):
            validation_errors = validation_errors[0: -1]

        return validation_errors
