from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.db.models import Count
from timeline.models import *


@login_required
def index(request):
	user = request.user

	study_list = user.studies.order_by("-date", "-created_at")
	# study_list = LatestStudy.objects.filter(user=user)
	for study in study_list:
		study.cat = study.get_category_names()

	timeline = user.timeline_set.all()[0]
	viewer_IDs = [ each.id for each in timeline.viewers.all()]


	context = {
		'study_list' : study_list,
		'categories' : user.category_set.all(),
		'viewer_IDs' : viewer_IDs,
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
	cats = Category.objects.filter(user=user).annotate(num_study=Count('study'))
	# 풀어쓰면 아래와 같음
	# categories = user.category_set.all()
	# for cat in categories:
	# 	cat.studynum = user.studies.filter(category=cat).count()

	context = {
		'categories' : cats
	}
	return render(request, 'timeline/cal.html', context)

# 쿼리셋의 각 아이템 별 개수 세기
# http://stackoverflow.com/questions/5439901/getting-a-count-of-objects-in-a-queryset-in-django
