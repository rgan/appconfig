from appconfig.models.app_environment import AppEnvironment
from appconfig.models.application import Application
from tests.unit.testmodels.base_db_test_case import DbTestBase

class AppEnvironmentTest(DbTestBase):

    def test_should_save_env(self):
        app = Application(name="lms").save()
        AppEnvironment(name="usc-mat-sb01", app=app).save()

        self.assertEquals("usc-mat-sb01", AppEnvironment.objects(app=app)[0].name)

    def test_should_put_new_key_value(self):
        app = Application(name="lms").save()
        env = AppEnvironment(name="usc-mat-sb01", app=app).save()
        env.put_value("adobe_host", "foobar.com")

        env_from_db = AppEnvironment.objects(app=app)[0]
        self.assertIsNotNone(env_from_db)
        entry = env_from_db.entries.get("adobe_host")
        self.assertIsNotNone(entry)
        self.assertEquals("foobar.com", entry.value)

    def test_should_update_key_value(self):
        app = Application(name="lms").save()
        env = AppEnvironment(name="usc-mat-sb01", app=app).save()
        env.put_value("adobe_host", "foobar.com")
        env.put_value("adobe_host", "foobar.com")

        env_from_db = AppEnvironment.objects(app=app)[0]
        self.assertEquals("foobar.com", env_from_db.entries.get("adobe_host").value)

    def test_should_get_value(self):
        app = Application(name="lms").save()
        env = AppEnvironment(name="usc-mat-sb01", app=app).save()
        env.put_value("adobe_host", "foobar.com")

        env_from_db = AppEnvironment.objects(app=app)[0]
        self.assertEquals("foobar.com", env_from_db.get_value("adobe_host"))

    def test_should_return_true_if_key_exists(self):
        app = Application(name="lms").save()
        env = AppEnvironment(name="usc-mat-sb01", app=app).save()
        env.put_value("adobe_host", "foobar.com")

        env_from_db = AppEnvironment.objects(app=app)[0]
        self.assertTrue(env_from_db.has_key("adobe_host"))
