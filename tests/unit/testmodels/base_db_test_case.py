import unittest
from appconfig.models.app_environment import AppEnvironment
from appconfig.models.application import Application
from mongoengine import connect

class DbTestBase(unittest.TestCase):

    def setUp(self):
        connect("test", host='mongodb://localhost/appconfig_test')

    def tearDown(self):
        self.deleteAll(AppEnvironment)
        self.deleteAll(Application)

    def deleteAll(self, cls):
        for o in cls.objects.all():
            o.delete()