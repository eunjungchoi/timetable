from django.shortcuts import render
from timeline.models import *
# Create your views here.




def index(request):
	study_list = Study.objects.all().order_by('date')
	for study in study_list:
		study.cats = []
		study.cats.append(study.cat01)
		study.cats.append(study.cat02)
		study.cats.append(study.cat03)
		study.cats.append(study.cat04)
		study.cats.append(study.cat05)

	context = {
		'study_list' : study_list,
	}

	return render(request, 'timeline/index.html', context)