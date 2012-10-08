import json
from appconfig.models.application import Application
import tornado.web

class EnvironmentHandler(tornado.web.RequestHandler):

    def put(self, app_name):
        env_name = json.loads(self.request.body)["name"]
        app = Application.find(app_name)
        if app is None:
            raise HTTPError(400, log_message="app not found %s" % app_name)
        if app.get_env(env_name) is not None:
            raise HTTPError(400, log_message="app name %s exists" % env_name)
        app.create_env(env_name)
        self.set_status(201)