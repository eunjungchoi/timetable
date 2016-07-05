from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template import loader
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse
from django.db.models import Q
from timeline.models import *



@login_required
def account(request, user_id):
	try:
		user = User.objects.get(pk=user_id)
	except User.DoesNotExist:
		return render(request, '404.html')

	try:
		timeline = Timeline.objects.get(owner=user)
	except Timeline.DoesNotExist:
		return render(request, '404.html')

	same_user = request.user.pk == user.pk
	has_permission = timeline.followers.filter(id=request.user.id).exists()

	if (not same_user) and (not has_permission):
		return render(request, '403.html')

	study_list = Study.objects.filter(user=user).order_by('-date')
	for study in study_list:
		study.cat = [ each_cat.name for each_cat in study.category.all()]
	
	categories = Category.objects.filter(user=user)

	context = {
		'study_list' : study_list,
		'categories' : categories,
		'user' : request.user,
	}
	return render(request, 'timeline/index.html', context)


@login_required
def add_follower(request):
	try:
		timeline = Timeline.objects.get(owner=request.user)
	except:
		timeline = Timeline(
			owner=request.user
			)
		timeline.save

	user = request.user
	follower_id = int(request.POST['follower_id_to_add'])


	try:
		follower = User.objects.get(pk=follower_id)
		if follower is request.user:
			follower = None

		elif not user.followings.filter(id=follower_id).exists():
			# follower = User.objects.get(pk=follower_id)
			timeline.followers.add(follower)
	except: 
		follower = None

	# if not user.followings.filter(id=follower_id).exists():
	# 	timeline.followers.add(follower)

	return redirect(reverse('index'))


@login_required
def delete_follower(request):
	follower_id_list_to_del = request.POST.getlist('each_id_to_del')
	user = request.user

	for each_id in follower_id_list_to_del:
		follower = User.objects.get(pk=int(each_id))
		timeline = Timeline.objects.get(owner=request.user)
		timeline.followers.remove(follower)
		# timeline.followers = timeline.followers.exclude(id=follower.id)


		# user.followings.filter(followers=follower).delete()
		# timeline.followers.get(user_id=each_id).delete()
		# each_follower = timeline.followers.get(id=int(each_id))
		# each_follower.delete()  <= 이렇게 하면 user 인스턴스가 통째로 삭제됨. 본의 아니게 남의 계정을 삭제하는 부작용
	
	return redirect(reverse('index'))

