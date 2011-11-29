from django.core.paginator import Paginator, InvalidPage
from core.models import *
from mongoengine import *
from mongoengine.fields import GridFSProxy
import random, os

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

    def get_rand(self):
        #if not rand:
        #    rand == rand
        result = {}
        item_list = []

        object_list = document.objects.all()
        object_length = len(object_list)
        rand = random.randint(0, object_length - 1)
  
        score = 0
        vote_list = []

        if len(object_list[rand]['vote_list']) > 1:
            for vote in object_list[rand]['vote_list']:
                vote_list.append(vote['rating'])
            score = sum(vote_list)/len(vote_list)
        dataset = {
            "id": str(object_list[rand]['id']),
            "name": object_list[rand]['name'],
            "description":object_list[rand]['description'],
            "image" : '/render/' + str(object_list[rand]['image']['id']),
            "vote_list": vote_list,
            "score": score
        }
        item_list.append(dataset)
        result['data'] = item_list
        return result


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

        result['paging'] = {
            'has_next_page' : page_obj.has_next()
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
                "vote_list": vote_list,
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
            v = vote(rating = int(r['rating']))
            v.save()
            d.vote_list.append(v)
            d.save()
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