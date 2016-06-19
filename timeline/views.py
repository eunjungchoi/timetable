from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template import loader
from django.shortcuts import render, redirect
from timeline.models import *



def index(request):
	study_list = Study.objects.all().order_by('date')
	categories = Category.objects.all()

	context = {
		'study_list' : study_list,
		'categories' : categories
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
	s = Study(
		title=request.POST['title'],
		date=request.POST['date'], 
		category=request.POST.getlist('category')
		)
	s.save()

	return redirect('/')
	



	# study_list = Study.objects.all().order_by('date')
	# categories = Category.objects.all()

	# context = {
	# 		'study_list' : study_list,
	# 	}

	# return render(request, 'timeline/index.html', context)

	# for study in study_list:
	# 	study.cats = []
	# 	study.cats.append(study.cat01)
	# 	study.cats.append(study.cat02)
	# 	study.cats.append(study.cat03)
	# 	study.cats.append(study.cat04)
	# 	study.cats.append(study.cat05)

		# cat02=request.POST['cat02'],
		# cat03=request.POST['cat03'],
		# cat04=request.POST['cat04'],
		# cat05=request.POST['cat05'],
		# cat06=request.POST['cat06'],
		# cat07=request.POST['cat07'],
		# cat08=request.POST['cat08'],
		# cat09=request.POST['cat09'],
		# cat10=request.POST['cat10']