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
	# study_list = LatestStudy.objects.filter(user=user)
	for study in study_list:
		study.cat = study.get_category_names()

	context = {
		'study_list' : study_list,
		'categories' : user.category_set.all(),
		}
	return render(request, 'timeline/index.html', context)


# 다른 방법. (오래 걸림)
	# response = requests.request('GET', url,
	# 	params={'redirect':0, 'access_token': social.extra_data['access_token']}
	# 	)
	# response.raise_for_status()
	# profile_picture_url = response.json()['data']['url']


@login_required
def detail(request, study_id):
	study = get_object_or_404(Study, pk=study_id)
	owner = get_object_or_404(User, pk=study.user.id)
	timeline = get_object_or_404(Timeline, owner=owner)

	is_owner = request.user.pk == owner.pk
	has_permission = timeline.viewers.filter(id=request.user.id).exists()

	if not (is_owner or has_permission):
		return render(request, '403.html')

	study.cat = study.get_category_names()
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
	default_day = today - timedelta(days=30)

	categories = []
	for cat in cats:
		item = {
			"name": cat.name,
			"num_study": cat.num_study,
			# "studies" : [0] * 30,
			# "date" : [today - timedelta(days=x) for x in reversed(range(30))]
			"studies" : [[today - timedelta(days=x), 0] for x in reversed(range(30))],
		}

		recent_study_list = user.studies.filter(date__gte=default_day).filter(category=cat)
		for study in recent_study_list:
			d = study.date - default_day
			x = d.days
			item["studies"][x][1] += 1

		categories.append(item)



	# cal_dict = {
	# 	"파이썬" : [0] * 30,
	# 	"장고" : [1] * 30,
	# }
	#
	# cats = Category.objects.filter(user=user).annotate(num_study=Count('study'))

	# 풀어쓰면 아래와 같음
	# categories = user.category_set.all()
	# for cat in categories:
	# 	cat.studynum = user.studies.filter(category=cat).count()

	context = {
		'categories' : categories,
		'month' : month,
		'default_day': default_day,
		'recent_study_list' : recent_study_list
		# 'cal_dict' : cal_dict
	}
	return render(request, 'timeline/cal.html', context)

# 쿼리셋의 각 아이템 별 개수 세기
# http://stackoverflow.com/questions/5439901/getting-a-count-of-objects-in-a-queryset-in-django
