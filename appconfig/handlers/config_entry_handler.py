import json
from appconfig.models.application import Application
import tornado.web

class ConfigEntryHandler(tornado.web.RequestHandler):

    def put(self, app_name, env_name):
        data = json.loads(self.request.body)
        env = self.get_env(app_name, env_name)
        env.put_value(data["key"], data["value"])
        self.set_status(201)

    def get(self, app_name, env_name, key):
        self.set_header("Content-Type", "application/json;charset=utf-8")
        env = self.get_env(app_name, env_name)
        if env.has_key(key):
            self.write(json.dumps(env.get_value(key)))
        else:
            raise HTTPError(400, log_message="key not found %s" % key)

    def get_env(self, app_name, env_name):
        app = Application.find(app_name)
        if app is None:
            raise HTTPError(400, log_message="app not found %s" % app_name)
        env = app.get_env(env_name)
        if env is None:
            raise HTTPError(400, log_message="env  %s not found" % env_name)
        return env


