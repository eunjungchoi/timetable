"""timetable URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from timeline import views
# from timeline.views import *


urlpatterns = [
    url(r'', include('social.apps.django_app.urls', namespace='social')),
    url(r'^admin/', admin.site.urls),
    url(r'^login/$', views.auth.log_in, name='log_in'),
    url(r'^logout/$', views.auth.log_out, name='log_out'),
    url(r'^$', views.home.index, name='index'),
    url(r'^(?P<study_id>[0-9]+)$', views.home.detail, name='detail'),
    url(r'^user/(?P<user_id>[0-9]+)$', views.viewer.account, name='account'),
    url(r'^add-viewer/$', views.viewer.add, name='add_viewer'),
    url(r'^delete-viewer/$', views.viewer.delete, name='delete_viewer'),
    url(r'^add/$', views.study.add, name='add'),
    url(r'^editform/(?P<study_id>[0-9]+)/$', views.study.editform, name='editform'),
    url(r'^edit/$', views.study.edit, name='edit'),
    url(r'^search/$', views.search.search, name='search'),
    url(r'^add-cat/$', views.category.add, name='add_cat'),
    url(r'^delete-cat/$', views.category.delete, name='delete_cat'),
    url(r'^delete/$', views.study.delete, name='delete'),
    url(r'^delete-each/(?P<study_id>[0-9]+)$', views.study.delete_each, name='delete_each'), 
    url(r'^cal/$', views.home.cal, name='cal'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# 마지막 static 라인은, debug= True일 때만 동작. 
