from django.conf.urls import url
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    url(r'^$', views.index),
    url(r'^projects$', views.projects),
    url(r'^createproject$', views.createproject),
    url(r'^newproject$', views.newproject),
    url(r'^trending$', views.trending),
    url(r'^signup$', views.signup),
    url(r'^signin$', views.signin),
    url(r'^login$', views.login),
    url(r'^users$', views.users),
    url(r'^logout$', views.logout),
    url(r'^register$', views.register),
    url(r'^newdonation$', views.newdonation),
    url(r'^project/(?P<id>\d+)$', views.project),
    url(r'^project/(?P<id>\d+)/donate$', views.donate)
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)