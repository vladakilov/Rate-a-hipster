from django.conf.urls.defaults import patterns, include, url
from django.conf import settings
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
		(r'^$',
		 'core.views.index'),
		
		(r'^doc/$',
		 'core.views.get_single_doc'),
		
    (r'^create/$',
     'core.views.create_doc_form'),

    (r'^vote/$',
     'core.views.rate_doc'),

    (r'^create_doc/$',
     'core.views.create_doc'),



    # Examples:
    # url(r'^$', 'api_test.views.home', name='home'),
    # url(r'^api_test/', include('api_test.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
