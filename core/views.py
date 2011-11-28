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
    form = document_form(request.POST)
    if form.is_valid():
        r = {'name': form.cleaned_data["name"],
             'description' : form.cleaned_data["description"]}
        response = doc_api.add(r)
    #return HttpResponse(str(doc_api.index(2)))
    return HttpResponse(str(response))

def rate_doc(request):
    doc_api = votes()
    r = {'rating': request.GET["rating"]}
    response = doc_api.create('4ecab5aac79eb90766000003', r)
    return HttpResponse(str(response))

def create_doc_form(request):
    form = document_form()
    t = loader.get_template("create_form.html")
    c = Context({'form':form})
    return HttpResponse(t.render(c))

def get_single_doc(request):
    doc_api = documents()
    return HttpResponse(json.dumps(doc_api.get_rand()), mimetype="application/json")
