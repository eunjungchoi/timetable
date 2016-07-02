from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template import loader
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse
from django.db.models import Q
from timeline.models import *



def log_in(request):
	if request.user.is_authenticated():
		return redirect(reverse('index'))
	return render(request, 'timeline/login.html')


@login_required
def log_out(request):
	logout(request)
	return redirect(reverse('log_in'))


@login_required
def index(request):
	study_list = Study.objects.filter(user=request.user).order_by('-date')
	for study in study_list:
		study.cat = [ each_cat.name for each_cat in study.category.all()]
	
	user = request.user

	categories = Category.objects.filter(user=request.user)

	try:
		timeline = Timeline.objects.get(owner=request.user)
		follower_IDs = [ each.id for each in timeline.followers.all()]
	except:
		timeline = None

	# followers = user.followings.all()
	# follower_list = []

	# for follower in followers:
	# 	follower_list += follower.id


	context = {
		'study_list' : study_list,
		'categories' : categories,
		'user' : user,
		'follower_IDs' : follower_IDs
	}
	return render(request, 'timeline/index.html', context)


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
	except :
		timeline = Timeline(
			owner=request.user
			)
		timeline.save

	follower_id = int(request.POST['follower_id'])
	follower = User.objects.get(pk=follower_id)

	user = request.user

	if not user.followings.filter(id=follower_id).exists():
	# if not user.followings.filter(followers=follower).exists():
		timeline.followers.add(follower)

		# timeline=Timeline(
		# 	owner=request.user,
		# 	followers=follower
		# 	)
		# timeline.save

		# user.followings.add(follower)
		
	return redirect(reverse('index'))


@login_required
def delete_follower(request):
	follower_id_list_to_del = request.POST.getlist('follower_name')
	
	for follower_id in follower_id_list_to_del:
		each = Timeline.objects.filter(owner=request.user).get(pk=follower_id)
		each.delete()

	return redirect(reverse('index'))


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


@login_required
def search(request):
	study_list = Study.objects.filter(user=request.user).order_by('-date')
	q = request.GET.get("q", None)
	if q:
		search_list = study_list.filter(Q(contents__icontains=q) | Q(title__icontains=q))
	else:
		search_list = []

	context = {
		'search_list' : search_list,
		'query': q
	}
	return render(request, 'timeline/search_result.html', context)


@login_required
def add(request):
	categories = Category.objects.filter(user=request.user)

	s = Study(
		user=request.user,
		title=request.POST['title'],
		date=request.POST['date'],
		contents=request.POST['contents']
		)
	s.save()

	cat_list = request.POST.getlist('category')

	for cat in cat_list:
		each_cat = Category.objects.filter(user=request.user).get(name=cat)
		s.category.add(each_cat)

	return redirect(reverse('index'))


@login_required
def edit(request):
	study_id = request.POST['study_id']
	s = Study.objects.get(pk=study_id)
	s.title = request.POST['title']
	s.date = request.POST['date']
	s.save()

	cat_list = request.POST.getlist('category')
	for cat in cat_list:
		each_cat = Category.objects.filter(user=request.user).get(name=cat)
		s.category.add(each_cat)
	return redirect(reverse('index'))


@login_required
def delete(request):
	s_list = request.POST.getlist('item')
	
	for study_id in s_list:
		each = Study.objects.filter(user=request.user).get(id=study_id)
		each.delete()

	return redirect(reverse('index'))


@login_required
def delete_each(request, study_id):
	s = Study.objects.filter(user=request.user).get(id=study_id)
	s.delete()

	return redirect(reverse('index'))


@login_required
def catadd(request):
	c = Category(
	user=request.user,
	name=request.POST['name'],
	)
	c.save()

	return redirect(reverse('index'))


@login_required
def catdelete(request):
	cat_id_list_to_del = request.POST.getlist('cat_name')
	
	for cat_id in cat_id_list_to_del:
		each = Category.objects.filter(user=request.user).get(id=cat_id)
		each.delete()

	return redirect(reverse('index'))


@login_required
def editform(request, study_id):
	categories = Category.objects.filter(user=request.user)
	study = Study.objects.filter(user=request.user).get(pk=study_id)
	study.cat = study.get_category_names()

	context = {
		'study' : study,
		'categories': categories
	}
	return render(request, 'timeline/editform.html', context)

