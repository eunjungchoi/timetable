from django.shortcuts import render
from timeline.models import *
# Create your views here.




def index(request):
	study_list = Study.objects.all().order_by('date')
	context = {
		'study_list' : study_list,
	}

	return render(request, 'timeline/index.html', context)