from mongoengine import *

class file_asset(Document):
    raw_file = FileField()
    file_type = StringField()

class vote(Document):
    rating = IntField(required=True)
  
class document(Document):
    name = StringField(required=True)
    description  = StringField(required=False)
    vote_list = ListField(GenericReferenceField(vote))
    image = ReferenceField(file_asset)