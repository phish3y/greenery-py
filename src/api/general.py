from pyramid.response import Response
from pyramid.request import Request

from datetime import datetime

from util.http import build_success_response, build_error_response, get_json_body_from_request, get_greenery_id_from_json_body
from util.s3 import S3
from util.logger import Logger


class General:

    def __init__(self):
        self.s3 = S3('greenery-data', 'general')
        self.required_general_json_keys = ['greenery_id', 'name', 'phone', 'email', 'address']
        self.logger = Logger()

    # /readGeneral
    def read_general(self, request: Request) -> Response:
        start = datetime.now()
        self.logger.log_info(request)
        if request.method != "POST":
            self.logger.log_error('/readGeneral requires POST http method')
            return build_error_response(400, '/readGeneral requires POST http method')

        self.logger.log_info('Beginning /readGeneral endpoint processing')
        json_body = get_json_body_from_request(request)
        if len(json_body) < 1:
            self.logger.log_error('Request body is not valid JSON!')
            return build_error_response(400, 'Request body is not valid JSON!')
        self.logger.log_info('parsed request body successfully')

        greenery_id = get_greenery_id_from_json_body(json_body)
        if len(greenery_id) < 1:
            self.logger.log_error("Request body must contain a populated 'greenery_id' field")
            return build_error_response(400, "Request body must contain a populated 'greenery_id' field")
        self.logger.log_info('extracted name {} from request body successfully'.format(greenery_id))

        s3_object: dict = self.s3.get_object_from_s3(greenery_id)
        if len(s3_object) < 1:
            self.logger.log_error('Failed to find {} in data store'.format(greenery_id))
            return build_error_response(404, 'Failed to find {} in data store'.format(greenery_id))
        self.logger.log_info('found general object {} in data store'.format(greenery_id))

        s3_content: str = self.s3.get_content_from_s3_object(s3_object)
        if len(s3_content) < 1:
            self.logger.log_error('Failed to read content from data store for {}'.format(greenery_id))
            return build_error_response(500, 'Failed to read content from data store for {}'.format(greenery_id))
        self.logger.log_info('read data from {} successfully'.format(greenery_id))

        response = build_success_response(s3_content)

        self.logger.log_info('Finished successfully. Took: {}'.format(datetime.now() - start))
        return response

    # /createGeneral
    def create_general(self, request: Request) -> Response:
        start = datetime.now()
        print(request)
        if request.method != "POST":
            self.logger.log_error('/createGeneral requires POST http method')
            return build_error_response(400, '/createGeneral requires POST http method')
        self.logger.log_info('Beginning /createGeneral endpoint processing')

        json_body: dict = get_json_body_from_request(request)
        if len(json_body) < 1:
            self.logger.log_error('Request body is not valid JSON!')
            return build_error_response(400, 'Request body is not valid JSON!')
        self.logger.log_info('parsed request body successfully')

        validation_errors: str = self.__validate_create_general_body(json_body)
        if len(validation_errors) > 0:
            self.logger.log_error(validation_errors)
            return build_error_response(400, validation_errors)
        self.logger.log_info('validated request body')

        greenery_id = get_greenery_id_from_json_body(json_body)
        if len(greenery_id) < 1:
            self.logger.log_error("Request body must contain a populated 'greenery_id' field")
            return build_error_response(400, "Request body must contain a populated 'greenery_id' field")
        self.logger.log_info('extracted name {} from request body successfully'.format(greenery_id))

        if not self.s3.create_s3_object(greenery_id, str(json_body)):
            self.logger.log_error('Failed to create new content in data store for {}'.format(greenery_id))
            return build_error_response(500, 'Failed to create new content in data store for {}'.format(greenery_id))
        self.logger.log_info('created new content successfully')

        response = build_success_response()
        self.logger.log_info('Finished successfully. Took: {}'.format(datetime.now() - start))
        return response

    def __validate_create_general_body(self, json_body: dict) -> str:
        validation_errors = ''
        for required_key in self.required_general_json_keys:
            if required_key not in json_body.keys():
                validation_errors += '{} is a required key in request body;'.format(required_key)

        if validation_errors.endswith(';'):
            validation_errors = validation_errors[0: -1]

        return validation_errors
