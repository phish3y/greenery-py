from wsgiref.simple_server import make_server
from pyramid.config import Configurator

from api.general import General


if __name__ == '__main__':
    general_api = General()
    with Configurator() as config:
        config.add_route('readGeneral', '/readGeneral')
        config.add_route('createGeneral', '/createGeneral')
        config.add_view(general_api.read_general, route_name='readGeneral')
        config.add_view(general_api.create_general, route_name='createGeneral')
        app = config.make_wsgi_app()
    server = make_server('0.0.0.0', 5000, app)
    print('server started')
    server.serve_forever()
