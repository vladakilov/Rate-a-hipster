from mongoengine import *
import datetime

class file_asset(Document):
    raw_file = FileField()
    file_type = StringField()

class vote(Document):
    rating = IntField(required=True)
    date_created = DateTimeField(default=datetime.datetime.now)
  
class document(Document):
    name = StringField(required=True)
    description  = StringField(required=False)
    vote_list = ListField(GenericReferenceField(vote))
    image = ReferenceField(file_asset)
    date_created = DateTimeField(default=datetime.datetime.now)