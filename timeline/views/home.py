from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

from timeline.models import *


@login_required
def index(request):
	user = request.user

	study_list = user.studies.order_by("-date", "-created_at")
	# study_list = LatestStudy.objects.filter(user=user)
	for study in study_list:
		study.cat = study.get_category_names()
	
	# categories = Category.objects.filter(user=request.user)

	# try: 
	# timeline = Timeline.objects.get(owner=request.user)
	timeline = user.timeline_set.all()[0]
	viewer_IDs = [ each.id for each in timeline.viewers.all()]
	# except Timeline.DoesNotExist:
	# 	viewer_IDs = []
	
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

	# if (not is_owner) and (not has_permission):
	if not (is_owner or has_permission):
		return render(request, '403.html')

	study.cat = study.get_category_names()
	context = {
		'study' : study,
		'owner' : owner,
		'same_user' : is_owner,
	}
	return render(request, 'timeline/detail.html', context)
