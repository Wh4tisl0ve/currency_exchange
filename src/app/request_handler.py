from src.app.exceptions.validation_error import ValidationError
from src.app.exceptions.not_found_error import NotFoundError
from src.app.router import Router
from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse
import json


class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        try:
            handler, params = Router().resolve(urlparse(self.path).path, method='GET')
            query_params = parse_qs(urlparse(self.path).query)

            if query_params:
                query_params = {k: v[0] for k, v in query_params.items()}
                params = query_params
                response = handler(params)
            else:
                response = handler(**params)
        except NotFoundError as endpoint_not_found:
            response = endpoint_not_found.to_dict()
        except TypeError:
            response = ValidationError('Endpoint does not accept parameters', 400).to_dict()

        self.__send_response(response['code'], 'application/json', json.dumps(response['body'], indent=4))

    def do_POST(self) -> None:
        params = self.get_params()
        try:
            handler = Router().resolve(self.path, method='POST')[0]
            response = handler(params)
        except NotFoundError as endpoint_not_found:
            response = endpoint_not_found.to_dict()
        except TypeError:
            response = ValidationError('Endpoint does not accept parameters', 400).to_dict()

        self.__send_response(response['code'], 'application/json', json.dumps(response['body'], indent=4))

    def do_PATCH(self) -> None:
        params = self.get_params()
        params['path'] = self.path

        try:
            handler = Router().resolve(self.path, method='PATCH')[0]
            response = handler(params)
        except NotFoundError as endpoint_not_found:
            response = endpoint_not_found.to_dict()
        except TypeError:
            response = ValidationError('Endpoint does not accept parameters', 400).to_dict()

        self.__send_response(response['code'], 'application/json', json.dumps(response['body'], indent=4))

    def do_OPTIONS(self):
        self.send_response(200, "ok")
        self.__send_headers(access_control_allow_headers="X-Requested-With, Content-Type")

    def get_params(self) -> dict:
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        params = parse_qs(post_data.decode('utf-8'))
        params = {k: v[0] for k, v in params.items()}
        return params

    def __send_headers(self, content_type='application/json',
                       access_control_allow_methods='GET, POST, PATCH, OPTIONS',
                       access_control_allow_headers='Content-Type',
                       access_control_allow_credentials='true',
                       access_control_allow_origin='*'):
        self.send_header('Access-Control-Allow-Credentials', access_control_allow_credentials)
        self.send_header('Access-Control-Allow-Methods', access_control_allow_methods)
        self.send_header('Access-Control-Allow-Headers', access_control_allow_headers)
        self.send_header('Access-Control-Allow-Origin', access_control_allow_origin)
        self.send_header('Content-type', content_type)
        self.end_headers()

    def __send_response(self, code, content_type, body) -> None:
        self.send_response(code)
        self.__send_headers(content_type)
        self.wfile.write(body.encode('utf-8'))
