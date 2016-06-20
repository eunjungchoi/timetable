from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template import loader
from django.shortcuts import render, redirect
from timeline.models import *



def index(request):
	study_list = Study.objects.all().order_by('date')
	for study in study_list:
		study.cat = [ each_cat.name for each_cat in study.category.all()]
	categories = Category.objects.all()

	context = {
		'study_list' : study_list,
		'categories' : categories,
	}

	return render(request, 'timeline/index.html', context)



def form(request):
	categories = Category.objects.all()
	template = loader.get_template('timeline/form.html')
	context = {
		'categories' : categories
	}
	return HttpResponse(template.render(context, request))


def add(request):
	categories = Category.objects.all()

	s = Study(
		title=request.POST['title'],
		date=request.POST['date']
		)
	s.save()


	cat_list = request.POST.getlist('category')

	for cat in cat_list:
		each_cat = Category.objects.get(name=cat)
		s.category.add(each_cat)

	return redirect('/')
