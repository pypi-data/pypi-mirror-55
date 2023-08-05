from django.conf.urls import include, url

urlpatterns = [
    url(r'^', include('aristotle_mdr.urls')),
    url(r'^browse/', include('aristotle_mdr.contrib.browse.urls')),
    url(r'^help/', include(('aristotle_mdr.contrib.help.urls', "aristotle_help"), namespace="aristotle_help")),
    url(r'^api/', include('aristotle_mdr_api.urls'))
]
