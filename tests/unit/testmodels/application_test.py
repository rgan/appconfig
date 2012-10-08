from mongoengine import connect
from appconfig.models.app_environment import AppEnvironment
from appconfig.models.application import Application
from tests.unit.testmodels.base_db_test_case import DbTestBase

class ApplicationTest(DbTestBase):

    def test_should_create_app(self):
        app = Application.create("lms")
        self.assertEquals("lms", Application.objects()[0].name)

    def test_should_return_true_if_app_name_exists(self):
        app = Application(name="lms").save()
        self.assertTrue(Application.name_exists("lms"))
        self.assertFalse(Application.name_exists("foobar"))

    def test_should_find_app_by_name(self):
        app = Application(name="lms").save()
        self.assertEquals("lms", Application.find("lms").name)

    def test_should_get_env(self):
        app = Application(name="lms").save()
        env = AppEnvironment(name="usc-mat-sb01", app=app).save()

        env_from_db = app.get_env("usc-mat-sb01")
        self.assertIsNotNone(env_from_db)

        env_from_db = app.get_env("non-existent-env")
        self.assertIsNone(env_from_db)

    def test_should_create_env(self):
        app = Application(name="lms").save()

        app.create_env("usc-mat-sb01")

        env_from_db = AppEnvironment.objects(app=app)[0]

        self.assertIsNotNone(env_from_db)




