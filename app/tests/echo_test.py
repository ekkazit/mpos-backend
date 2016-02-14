from . import BaseTest
from flask import json


class EchoTest(BaseTest):
    def test_echo_print_api(self):
        resp = self.client.get('/api/echo/print')
        data = json.loads(resp.data)
        assert resp.status_code == 200
        assert data['echo'] == 'echo from api'
