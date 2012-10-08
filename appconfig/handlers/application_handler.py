import json
from appconfig.models.application import Application
from tornado.web import HTTPError, RequestHandler

class ApplicationHandler(RequestHandler):

    def put(self):
        name = json.loads(self.request.body)["name"]
        if Application.name_exists(name):
            raise HTTPError(400, log_message="app name %s exists" % name)
        Application.create(name)
        self.set_status(201)
