from django.core.paginator import Paginator, InvalidPage
from core.models import *
from mongoengine import *
from mongoengine.fields import GridFSProxy
import random, os, json

class api_base:
    object_id = None
    count = 5
    def set_object_id(self, object_id):
        self.object_id = object_id
    
class documents(api_base):
    
    def add(self, item):
        result = {}
        doc = document()
        util = utils()
        try:
            doc.name = item['name']
            doc.description = item['description']
            doc.image = util.upload(item['image'])
            doc.save()
            result['data'] = doc.id
        except Exception as e:
            result['error'] = str(e)
        return result

    def get_doc(self, obj_id=None):
        result = {}
        vote_list = []
        item_list = []
        score = 0
  
        if not obj_id is None:
            obj_id == obj_id
            object_list = document.objects(id=obj_id)
            i = 0
        else:
            object_list = document.objects.all()
            i = random.randint(0, len(object_list) - 1)

        if len(object_list[i]['vote_list']) > 1:
            for vote in object_list[i]['vote_list']:
                vote_list.append(vote['rating'])
            score = sum(vote_list)/len(vote_list)
        dataset = {
            "id": str(object_list[i]['id']),
            "name": object_list[i]['name'],
            "description":object_list[i]['description'],
            "image" : '/render/' + str(object_list[i]['image']['id']),
            "vote_list": vote_list,
            "score": score
        }
        item_list.append(dataset)
        result['data'] = item_list
        return json.dumps(result)


    def index(self, page=1):
        result = {}
        item_list = []
        vote_list = []
        if not page is None:
          page == page
        object_list = document.objects.all()
        paginator = Paginator(object_list, self.count)
        try:
            page_obj = paginator.page(page)
        except InvalidPage:
            return result
        if page_obj.has_next():
            result['paging'] = {
                'page_list' : paginator.page_range,
                'next_page' : page_obj.next_page_number()
        }
        if page_obj.has_previous():
            result['paging'] = {
                'page_list' : paginator.page_range,
                'previous_page' : page_obj.previous_page_number(),
        }
        if page_obj.has_next() and page_obj.has_previous():
            result['paging'] = {
                'page_list' : paginator.page_range,
                'previous_page' : page_obj.previous_page_number(),
                'next_page' : page_obj.next_page_number()
        }
        score = 0
        for item in object_list:
            if 'vote_list' in item and len(item.vote_list) > 1:
                for vote in item.vote_list:
                    vote_list.append(vote['rating'])
                score = sum(vote_list)/len(vote_list)
            dataset = {
                "id": str(item.id),
                "name": item.name,
                "description":item.description,
                "image" : '/render/' + str(item.image.id),

                #"vote_list": vote_list,
                "score": score
            }
            item_list.append(dataset)
        result['data'] = item_list
        return result

class voting(api_base):
    
    def create(self, obj_id, r):
        result = {}
        d = document.objects.with_id(obj_id)
        try:
            if 0 < int(r['rating']) <= 10:
                v = vote(rating = int(r['rating']))
                v.save()
                d.vote_list.append(v)
                d.save()
            else:
                raise NameError('Votes must be in between the range 1 - 10.')
        except Exception as e:
            result['error'] = str(e)
        return result

class utils():
    
    def upload(self, f):
        random_num = random.randint(1, 10000)
        destination = open('/tmp/' + str(random_num), 'wb+')
    
        for chunk in f.chunks():
          destination.write(chunk)
        destination.close()

        try:
          i = file_asset(raw_file = open('/tmp/' + str(random_num), 'r'))
          i.file_type = 'image/jpeg'
          i.save()

        except Exception as strerror:
            raise NameError(strerror)

        os.remove('/tmp/' + str(random_num))
        return i        