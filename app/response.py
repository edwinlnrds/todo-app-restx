from flask import make_response, jsonify


class Response(object):
    __instance = None

    def __new__(cls):
        if Response.__instance is None:
            Response.__instance = object.__new__(cls)
        return Response.__instance

    def __init__(self):
        self.payload = {
            'message': '',
            'status_code': None,
            'values': None
        }

    def create_payload_response(self, status_code, message, values):
        self.payload['message'] = message
        self.payload['status_code'] = status_code
        self.payload['values'] = values

        return make_response(jsonify(self.payload), self.payload['status_code'])

    def ok(self, message, values):
        return self.create_payload_response(200, message, values)

    def bad_request(self, message, values):
        return self.create_payload_response(400, message, values)

    def not_found(self, message, values):
        return self.create_payload_response(404, message, values)

    def unauthorized(self, message, values):
        return self.create_payload_response(401, message,  values)


response = Response()
