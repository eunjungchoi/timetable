from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from timeline.models import *



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