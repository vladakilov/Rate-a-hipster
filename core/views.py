from django.http import HttpResponse, HttpRequest
from django.template import Context, loader
from django.utils import simplejson
from django.conf import settings
from core.models import *
from core.document_form import *
from mongoengine import *
from datetime import *
from api import *
import json

def index(request):
    t = loader.get_template("index.html")
    c = Context({'form':'form'})
    return HttpResponse(t.render(c))

def create_doc(request):
    doc_api = documents()
    form = document_form(request.POST, request.FILES)
    try:
        response = {}
        if form.is_valid():
            r = {'name': form.cleaned_data["name"],
                 'description' : form.cleaned_data["description"],
                 'image' : request.FILES['image']}
            response = doc_api.add(r)
    except Exception as e:
        response = e
    return HttpResponse(str(response))

def create_doc_form(request):
    form = document_form()
    t = loader.get_template("create_form.html")
    c = Context({'form':form})
    return HttpResponse(t.render(c))

#api call to vote on a single doc response->json object
def rate_doc(request):
    vote_api = voting()
    r = {'rating': request.POST["rating"]}
    response = vote_api.create(request.POST["id"], r)
    return HttpResponse(json.dumps(response), mimetype="application/json")

#api call to show a random single doc response->json object
def get_rand_doc(request):
    doc_api = documents()
    return HttpResponse(doc_api.get_doc(), mimetype="application/json")

#api call to show single doc response->json object
def get_doc(request, obj_id):
    doc_api = documents()
    return HttpResponse(doc_api.get_doc(obj_id), mimetype="application/json")

#api call to show all docs response->json object
def list_docs(request):
    page = int(request.GET["page"])
    doc_api = documents()
    return HttpResponse(json.dumps(doc_api.index(page), sort_keys=True, indent=2), mimetype="application/json")

def render_doc(request, obj_id):
    doc_api = documents()
    t = loader.get_template("single_doc.html")
    c = Context({'doc': json.loads(doc_api.get_doc(obj_id))})
    return HttpResponse(t.render(c))

def render_asset(request, img_id):
    m = file_asset.objects.with_id(img_id)
    mime = m.file_type
    return HttpResponse(m.raw_file.read(),mimetype=mime)