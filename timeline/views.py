from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template import loader
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from timeline.models import *

def intro(request):
	if request.user.is_authenticated():
		return redirect('/index/')
	return render(request, 'timeline/intro.html')


@login_required
def index(request):
	study_list = Study.objects.filter(user=request.user).order_by('-date')
	for study in study_list:
		study.cat = [ each_cat.name for each_cat in study.category.all()]
	# header = "열심히 공부하고 있습니다"
	# msg = "오늘 공부 추가하기"
	
	categories = Category.objects.filter(user=request.user)
	# if len(categories) == 0:
	# 	header = "열심히 공부해볼까요?"
	# 	msg = "달력이 비어있네요. 먼저 요즘 어떤 공부를 하고 있는지 카테고리들을 먼저 추가하고, 날짜별 공부일정을 등록해보세요 "
	user = request.user

	context = {
		'study_list' : study_list,
		'categories' : categories,
		'user' : user,
		'header' : header,
		'msg' : msg
	}
	return render(request, 'timeline/index.html', context)


@login_required
def detail(request, study_id):
	if not request.user.is_authenticated():
		return render(request, 'timeline/intro.html')
	
	categories = Category.objects.filter(user=request.user)
	study = Study.objects.filter(user=request.user).get(pk=study_id)
	study.cat = [ each_cat.name for each_cat in study.category.all()]
	
	context = {
		'study' : study,
		'categories': categories
	}
	return render(request, 'timeline/detail.html', context)


@login_required
def log_out(request):
	logout(request)
	return redirect('/')


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

	return redirect('/index/')


@login_required
def edit(request):
	study_id = request.POST['study_id']
	s = Study.objects.get(pk=study_id)
	s.title = request.POST['title']
	s.date = request.POST['date']
#  이부분을 해야 됨. -------------------------------------------수정을 하긴 했는데, 원래 카테고리가 안 뜸-----
	s.save()

	cat_list = request.POST.getlist('category')

	for cat in cat_list:
		each_cat = Category.objects.filter(user=request.user).get(name=cat)
		s.category.add(each_cat)
	return redirect('/')

@login_required
def delete(request):
	s_list = request.POST.getlist('item')
	
	for study_id in s_list:
		each = Study.objects.filter(user=request.user).get(id=study_id)
		each.delete()

	return redirect('/index/')

@login_required
def delete_each(request, study_id):
	s = Study.objects.filter(user=request.user).get(id=study_id)
	s.delete()

	return redirect('/index/')


@login_required
def catadd(request):
	c = Category(
	user=request.user,
	name=request.POST['name'],
	)
	c.save()

	return redirect('/index/')


@login_required
def catdelete(request):
	cat_id_list_to_del = request.POST.getlist('cat_name')
	
	for cat_id in cat_id_list_to_del:
		each = Category.objects.filter(user=request.user).get(id=cat_id)
		each.delete()

	return redirect('/index/')


@login_required
def editform(request, study_id):
	categories = Category.objects.filter(user=request.user)
	study = Study.objects.filter(user=request.user).get(pk=study_id)
	context = {
		'study' : study,
		'categories': categories
	}
	return render(request, 'timeline/editform.html', context)

