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
from timeline import views


urlpatterns = [
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT, 'show_indexes': True, }),
    url(r'', include('social.apps.django_app.urls', namespace='social')),
    url(r'^admin/', admin.site.urls),
    url(r'^login/$', views.log_in, name='log_in'),
    url(r'^logout/$', views.log_out, name='log_out'),
    url(r'^$', views.index, name='index'),
    url(r'^user/(?P<user_id>[0-9]+)$', views.account, name='account'),
    url(r'^add-follower/$', views.add_follower, name='add_follower'),
    url(r'^delete-follower/$', views.delete_follower, name='delete_follower'),
    url(r'^(?P<study_id>[0-9]+)$', views.detail, name='detail'),
    url(r'^add/$', views.add, name='add'),
    url(r'^editform/(?P<study_id>[0-9]+)/$', views.editform, name='editform'),
    url(r'^edit/$', views.edit, name='edit'),
    url(r'^search/$', views.search, name='search'),
    url(r'^catadd/$', views.catadd, name='catadd'),
    url(r'^delete/$', views.delete, name='delete'),
    url(r'^delete-each/(?P<study_id>[0-9]+)$', views.delete_each, name='delete_each'), 
    url(r'^catdelete/$', views.catdelete, name='catdelete'),
]