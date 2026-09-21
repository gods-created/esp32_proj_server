from mongoengine import Document

class Base(Document):
    meta = {'allow_inheritance': True}