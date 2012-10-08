from tornado.options import define, options
import tornado.web
import tornado.ioloop
from appconfig.handlers.application_handler import ApplicationHandler
from appconfig.handlers.config_entry_handler import ConfigEntryHandler
from appconfig.handlers.environment_handler import EnvironmentHandler
from mongoengine import connect

define("dburl", default="mongodb://localhost/appconfig_test", help="URI to mongo db")

if __name__ == "__main__":
    tornado.options.parse_command_line()
    connect("appconfig", host=options.dburl)
    application = tornado.web.Application([
        (r"/apps", ApplicationHandler),
        (r"/apps/(?P<app_name>[\w]*)/environments", EnvironmentHandler),
        (r"/apps/(?P<app_name>[\w]*)/environments/(?P<env_name>[\w]*)/entries", ConfigEntryHandler),
        (r"/apps/(?P<app_name>[\w]*)/environments/(?P<env_name>[\w]*)/entries/(?P<key>[\w]*)", ConfigEntryHandler),
    ])
    application.listen(8000)
    tornado.ioloop.IOLoop.instance().start()