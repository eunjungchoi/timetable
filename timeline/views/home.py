from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.db.models import Count
from django.utils import timezone
from datetime import datetime, timedelta, date
from timeline.models import *


@login_required
def index(request):
	user = request.user
	study_list = user.studies.order_by("-date", "-created_at")
	context = {
		'study_list' : study_list,
		'categories' : user.category_set.all(),
		}
	return render(request, 'timeline/index.html', context)


@login_required
def detail(request, study_id):
	study = get_object_or_404(Study, pk=study_id)
	owner = study.user
	timeline = get_object_or_404(Timeline, owner=owner)

	is_owner = request.user.pk == owner.pk
	has_permission = timeline.viewers.filter(id=request.user.id).exists()

	if not (is_owner or has_permission):
		return render(request, '403.html')

	context = {
		'study' : study,
		'owner' : owner,
		'same_user' : is_owner,
	}
	return render(request, 'timeline/detail.html', context)


@login_required
def cal(request):
	user = request.user
	cats = user.category_set.annotate(num_study=Count('study'))
	month = range(30)
	today = date.today()
	default_day = today - timedelta(days=29)

	categories = []
	for cat in cats:
		item = {
			"name": cat.name,
			"num_study": cat.num_study,
			"studies" : [[today - timedelta(days=x), 0] for x in reversed(range(30))],
		}

		recent_study_list = user.studies.filter(date__gte=default_day).filter(category=cat)
		for study in recent_study_list:
			d = study.date - default_day
			x = d.days
			item["studies"][x][1] += 1

		categories.append(item)

	context = {
		'categories' : categories,
		'month' : month,
		'default_day': default_day,
		'recent_study_list' : recent_study_list
	}
	return render(request, 'timeline/cal.html', context)
