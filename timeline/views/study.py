from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from timeline.models import *


@login_required
def add(request):
	if not request.POST['title'] or not request.POST['date']:
		return redirect(reverse('index'))

	categories = Category.objects.filter(user=request.user)

	s = Study(
		user=request.user,
		title=request.POST['title'],
		date=request.POST['date'],
		contents=request.POST['contents'],
	)
	if 'photo' in request.FILES:
		s.pic = request.FILES['photo']
		s.resize_image(max_size=(720,720))
	s.save()

	cat_list = request.POST.getlist('category')
	for cat_id in cat_list:
		each_cat = Category.objects.filter(user=request.user).get(id=cat_id)
		s.category.add(each_cat)

	return redirect(reverse('index'))


@login_required
def editform(request, study_id):
	categories = Category.objects.filter(user=request.user)
	study = Study.objects.filter(user=request.user).get(pk=study_id)

	context = {
		'study' : study,
		'categories': categories
	}
	return render(request, 'timeline/editform.html', context)


@login_required
def edit(request):
	study_id = request.POST['study_id']
	s = Study.objects.get(pk=int(study_id))
	s.title = request.POST['title']
	s.date = request.POST['date']
	s.contents = request.POST['contents']
	s.save()

	cat_id_list = request.POST.getlist('category_id_to_edit')
	for cat_id in cat_id_list:
		cat = Category.objects.filter(user=request.user).get(id=int(cat_id))
		s.category.add(cat)
	return redirect(reverse('detail', kwargs={'study_id':study_id}))


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
