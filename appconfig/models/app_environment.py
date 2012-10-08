from mongoengine import Document, EmbeddedDocument, StringField, EmbeddedDocumentField,ReferenceField, MapField

class Entry(EmbeddedDocument):
    key = StringField()
    value = StringField()
    # additional metadata like type, time added/modified, user who modified etc.
    #type = StringField()

class AppEnvironment(Document):
    name = StringField()
    app = ReferenceField("Application")
    entries = MapField(EmbeddedDocumentField("Entry"))

    def has_key(self, key):
        return self.entries.get(key)

    def get_value(self, key):
        entry = self.entries.get(key, None)
        if entry is None:
            raise ValueError("Unknown key: %s" % key)
        return entry.value

    def put_value(self, key, value):
        entry = self.entries.get(key)
        if entry is None:
            self.entries[key] = Entry(key=key, value=value)
        else:
            entry.value = value
        self.save()


