from django.core.paginator import Paginator, InvalidPage
from core.models import *
from mongoengine import *

class api_base:
    object_id = None
    count = 5
    def set_object_id(self, object_id):
        self.object_id = object_id
    
class documents(api_base):
    
    def add(self, item):
        result = {}
        doc = document()
        try:
            doc.name = item['name']
            doc.description = item['description']
            doc.save()
            result['data'] = doc.id
        except Exception as e:
            result['error'] = str(e)
        return result
    """
    def handle_uploaded_file(self, f, p):
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
    """

    def get_rand(self):
        result = {}
        item_list = []

        object_list = document.objects.all()

        for item in object_list:
	
            score = 0
            vote_list = []

            if 'votes' in item and len(item.votes) > 1:
                for vote in item.votes:
                    vote_list.append(vote['rating'])
                score = sum(vote_list)/len(vote_list)
            dataset = {
                "id": str(item.id),
                "name": item.name,
                "description":item.description,
                "votes": vote_list,
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
            if 'votes' in item and len(item.votes) > 1:
                for vote in item.votes:
                    vote_list.append(vote['rating'])
                score = sum(vote_list)/len(vote_list)
            dataset = {
                "id": str(item.id),
                "name": item.name,
                "description":item.description,
                "votes": vote_list,
                "score": score
            }
            item_list.append(dataset)
        result['data'] = item_list
        return result

class votes(api_base):
    
    def create(self, obj_id, r):
        result = {}
        d = document.objects.with_id(str(obj_id))
        v = vote()
        try:
            v.rating = r['rating']
            v.save()
            d.votes.append(v)
            d.save()
            #result['data'] = d
        except Exception as e:
            result['error'] = str(e)
        return result
