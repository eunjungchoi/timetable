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
from timeline import views


urlpatterns = [
    url(r'', include('social.apps.django_app.urls', namespace='social')),
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.intro, name='intro'),
    url(r'^logout/$', views.log_out, name='log_out'),
    url(r'^index/$', views.index, name='index'),
    url(r'^(?P<study_id>[0-9]+)$', views.detail, name='detail'),
    url(r'^add/$', views.add, name='add'),
    url(r'^editform/(?P<study_id>[0-9]+)/$', views.editform, name='editform'),
    url(r'^edit/$', views.edit, name='edit'),
    url(r'^catadd/$', views.catadd, name='catadd'),
    url(r'^delete/$', views.delete, name='delete'),
    url(r'^delete-each/(?P<study_id>[0-9]+)$', views.delete_each, name='delete_each'), 
    url(r'^catdelete/$', views.catdelete, name='catdelete'),
]


# <a href="/edit/{{study_id}}/">수정</a><br>
