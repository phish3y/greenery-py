from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response
from pyramid.request import Request

import boto3

import traceback
import json
from datetime import datetime

s3_client = boto3.client('s3')


def build_error_response(code: int, message: str) -> Response:
    return Response(status=code,
                    content_type='application/json',
                    charset='UTF-8',
                    headerlist=[('Access-Control-Allow-Origin', '*')],
                    body='{ "message": "' + message + '" }')


def get_json_body_from_request(request: Request) -> dict:
    try:
        return request.json_body
    except:
        traceback.print_exc()
        return {}


def get_name_from_json_body(json_body: dict) -> str:
    try:
        return json_body['name']
    except:
        traceback.print_exc()
        return ''


def get_general_object_from_s3_by_name(name: str) -> dict:
    try:
        return s3_client.get_object(Bucket='greenery-data',
                                    Key='general/{}.json'.format(name))
    except:
        traceback.print_exc()
        return {}


def get_content_from_s3_object(s3_object: dict) -> str:
    try:
        return str(json.loads(s3_object['Body'].read()))
    except:
        traceback.print_exc()
        return ''


def read_general(request: Request) -> Response:
    start = datetime.now()
    print(request)
    if request.method != "POST":
        return build_error_response(400, '/readGeneral requires POST http method')

    print('Beginning /readGeneral endpoint processing')
    json_body = get_json_body_from_request(request)
    if len(json_body) < 1:
        return build_error_response(400, 'Request body is not valid JSON!')
    print('parsed request body successfully')

    name = get_name_from_json_body(json_body)
    if len(name) < 1:
        return build_error_response(400, "Request body must contain a populated 'name' field")
    print('extracted name {} from request body successfully'.format(name))

    s3_object: dict = get_general_object_from_s3_by_name(name)
    if len(s3_object) < 1:
        return build_error_response(404, 'Failed to find {} in data store'.format(name))
    print('found general object {} in data store'.format(name))

    s3_content: str = get_content_from_s3_object(s3_object)
    if len(s3_content) < 1:
        return build_error_response(500, 'Failed to read content from data store for {}'.format(name))
    print('read data from {} successfully'.format(name))

    try:
        response = Response(status=200,
                            content_type='application/json',
                            charset='UTF-8',
                            headerlist=[('Access-Control-Allow-Origin', '*')],
                            body=s3_content)
    except:
        traceback.print_exc()
        return build_error_response(500, "Failed to build response object with data from {}".format(name))

    print('Finished successfully. Took: {}'.format(datetime.now() - start))
    return response


required_general_json_keys = ['name', 'phone', 'email', 'address']


def validate_create_general_body(json_body: dict) -> str:
    validation_errors = ''
    for required_key in required_general_json_keys:
        if required_key not in json_body.keys():
            validation_errors += '{} is a required key in request body;'.format(required_key)

    if validation_errors.endswith(';'):
        validation_errors = validation_errors[0: -1]

    return validation_errors


def create_general_s3_object():
    # TODO
    pass


def create_general(request: Request) -> Response:
    start = datetime.now()
    print(request)
    if request.method != "POST":
        return build_error_response(400, '/createGeneral requires POST http method')
    print('Beginning /createGeneral endpoint processing')

    json_body = get_json_body_from_request(request)
    if len(json_body) < 1:
        return build_error_response(400, 'Request body is not valid JSON!')
    print('parsed request body successfully')

    validation_errors = validate_create_general_body(json_body)
    if len(validation_errors) > 0:
        print(validation_errors)
        return build_error_response(400, validation_errors)
    print('validated request body')

    create_general_s3_object()

    print('Finished successfully. Took: {}'.format(datetime.now() - start))
    return Response(status=200, body='wip')


if __name__ == '__main__':
    with Configurator() as config:
        config.add_route('readGeneral', '/readGeneral')
        config.add_route('createGeneral', '/createGeneral')
        config.add_view(create_general, route_name='createGeneral')
        app = config.make_wsgi_app()
    server = make_server('0.0.0.0', 5000, app)
    print('server started')
    server.serve_forever()
