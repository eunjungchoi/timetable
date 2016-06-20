from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template import loader
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from timeline.models import *

@login_required
def index(request):
	study_list = Study.objects.filter(user=request.user).order_by('date')
	for study in study_list:
		study.cat = [ each_cat.name for each_cat in study.category.all()]
	categories = Category.objects.filter(user_id=request.user)

	context = {
		'study_list' : study_list,
		'categories' : categories,
	}

	return render(request, 'timeline/index.html', context)



def form(request):
	categories = Category.objects.filter(user=request.user)
	template = loader.get_template('timeline/form.html')
	context = {
		'categories' : categories
	}
	return HttpResponse(template.render(context, request))


def add(request):
	categories = Category.objects.filter(user=request.user)

	s = Study(
		user=request.user,
		title=request.POST['title'],
		date=request.POST['date']
		)
	s.save()


	cat_list = request.POST.getlist('category')

	for cat in cat_list:
		each_cat = Category.objects.filter(user=request.user).get(name=cat)
		s.category.add(each_cat)

	return redirect('/')


def catform(request):
	# categories = Category.objects.all()
	template = loader.get_template('timeline/catform.html')
	context = {
	}
	return HttpResponse(template.render(context, request))



def catadd(request):
	c = Category(
	user=request.user,
	name=request.POST['name'],
	)
	c.save()

	return redirect('/')

