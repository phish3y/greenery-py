from pyramid.response import Response
from pyramid.request import Request

import traceback


def build_success_response(body: str = '') -> Response:
    try:
        return Response(status=200,
                        content_type='application/json',
                        charset='UTF-8',
                        headerlist=[('Access-Control-Allow-Origin', '*')],
                        body=body)
    except:
        traceback.print_exc()
        return build_error_response(500, "Failed to build success response object")


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


def get_greenery_id_from_json_body(json_body: dict) -> str:
    try:
        return json_body['greenery_id']
    except:
        traceback.print_exc()
        return ''
