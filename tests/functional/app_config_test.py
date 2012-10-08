from tornado.testing import *
from tornado.httpclient import HTTPRequest
from appconfig.models.app_environment import AppEnvironment
from appconfig.models.application import Application
from mongoengine import connect

class AppConfigTest(AsyncTestCase):

    def tearDown(self):
        connect("test", host='mongodb://localhost/appconfig_test')
        self.deleteAll(AppEnvironment)
        self.deleteAll(Application)

    def deleteAll(self, cls):
        for o in cls.objects.all():
            o.delete()

    def test_should_create_config_entry(self):
        client = AsyncHTTPClient(self.io_loop)

        http_request = HTTPRequest("http://localhost:8000/apps", method="PUT", body='{"name" : "lms"}')
        client.fetch(http_request, self.stop)
        response = self.wait();
        self.assertEquals(201, response.code)

        http_request = HTTPRequest("http://localhost:8000/apps/lms/environments", method="PUT", body='{"name" : "dev"}')
        client.fetch(http_request, self.stop)
        response = self.wait();
        self.assertEquals(201, response.code)

        http_request = HTTPRequest("http://localhost:8000/apps/lms/environments/dev/entries", method="PUT",
            body='{"key" : "adobe_host", "value" : "foobar.com" }')
        client.fetch(http_request, self.stop)
        response = self.wait();
        self.assertEquals(201, response.code)

        http_request = HTTPRequest("http://localhost:8000/apps/lms/environments/dev/entries/adobe_host", method="GET")
        client.fetch(http_request, self.stop)
        response = self.wait();
        self.assertEquals(200, response.code)
        print response.body
        self.assertEquals('"foobar.com"', response.body)

