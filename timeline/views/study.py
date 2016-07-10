from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect

from timeline.models import *


@login_required
def add(request):
	if not request.POST['title'] or not request.POST['date']:
		return redirect(reverse('index'))
	# input = None 처리 중, 4개 필드 모두 비워둔 상태로 등록 버튼을 눌렀을 경우만 먼저 처리 : 같은 페이지로 리다이렉트
	# 제목과 날짜가 default 입력 필드

	categories = Category.objects.filter(user=request.user)

	s = Study.objects.create(
		user=request.user,
		title=request.POST['title'],
		date=request.POST['date'],
		contents=request.POST['contents'],
		pic=request.FILES['photo'],
		)

	cat_list = request.POST.getlist('category')

	for cat in cat_list:
		each_cat = Category.objects.filter(user=request.user).get(id=cat.id)
		s.category.add(each_cat)

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


@login_required
def edit(request):
	study_id = request.POST['study_id']
	s = Study.objects.get(pk=study_id)
	s.title = request.POST['title']
	s.date = request.POST['date']
	s.contents = request.POST['contents']
	s.save()

	cat_list = request.POST.getlist('category')
	for cat in cat_list:
		each_cat = Category.objects.filter(user=request.user).get(id=cat.id)
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
