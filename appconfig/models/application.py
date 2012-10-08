from mongoengine import Document,StringField, Q
from appconfig.models.app_environment import AppEnvironment

class Application(Document):

    name = StringField()

    @classmethod
    def create(cls, name):
        if cls.name_exists(name):
            raise ValueError("Name exists")
        Application(name=name).save()

    @classmethod
    def name_exists(cls, name):
        return Application.objects(name=name)

    @classmethod
    def find(self, name):
        result = Application.objects(name=name)
        if result:
            return result[0]
        return None

    def get_env(self, env_name):
        result = AppEnvironment.objects((Q(name=env_name) & Q(app=self)))
        if len(result) > 0:
            return result[0]
        return None

    def create_env(self, env_name):
        AppEnvironment(name=env_name, app=self).save()

