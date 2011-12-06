from django.conf.urls.defaults import patterns, include, url
from django.conf import settings
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',

    #static content
    (r'^static/(?P<path>.*)$', 'django.views.static.serve',
    {'document_root': settings.STATIC_DOC_ROOT}),

    (r'^$',
    'core.views.index'),

    (r'^api/doc/$',
    'core.views.list_docs'),
        
    (r'^api/doc/(?P<obj_id>\w+)/$',
    'core.views.get_doc'),
        
    (r'^api/random/$',
    'core.views.get_rand_doc'),

    (r'^api/vote/$',
     'core.views.rate_doc'),

    (r'^doc/(?P<obj_id>\w+)/$',
    'core.views.render_doc'),
        
    (r'^create/$',
     'core.views.create_doc_form'),

    (r'^create_doc/$',
     'core.views.create_doc'),

    (r'^render/(?P<img_id>\w+)/$',
     'core.views.render_asset'),

    # Examples:
    # url(r'^$', 'api_test.views.home', name='home'),
    # url(r'^api_test/', include('api_test.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)