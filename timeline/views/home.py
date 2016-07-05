from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template import loader
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse
from django.db.models import Q
from timeline.models import *
import requests



@login_required
def index(request):
	study_list = Study.objects.filter(user=request.user).order_by('-date')
	for study in study_list:
		study.cat = [ each_cat.name for each_cat in study.category.all()]
	
	user = request.user
	try:
		social = user.social_auth.get()
		url = 'https://graph.facebook.com/{0}/picture?type=small'.format(social.uid)
	except:
		url = ''

	# 오래 걸림 
	# response = requests.request('GET', url, 
	# 	params={'redirect':0, 'access_token': social.extra_data['access_token']}
	# 	)
	# response.raise_for_status()
	# profile_picture_url = response.json()['data']['url']


	categories = Category.objects.filter(user=request.user)

	try: 
		 
		timeline = Timeline.objects.get(owner=request.user)
		follower_IDs = [ each.id for each in timeline.followers.all()]
	except:
		timeline = None
		follower_IDs = []
	
	context = {
		'study_list' : study_list,
		'categories' : categories,
		'user' : user,
		'follower_IDs' : follower_IDs,
		'profile_picture_url' : url
		}
	return render(request, 'timeline/index.html', context)


@login_required
def detail(request, study_id):
	categories = Category.objects.filter(user=request.user)
	study = Study.objects.filter(user=request.user).get(pk=study_id)
	study.cat = [ each_cat.name for each_cat in study.category.all()]
	
	context = {
		'study' : study,
		'categories': categories
	}
	return render(request, 'timeline/detail.html', context)
