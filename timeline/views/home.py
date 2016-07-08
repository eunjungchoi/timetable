from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

from timeline.models import *


@login_required
def index(request):
	user = request.user

	study_list = Study.objects.filter(user=user).order_by('-date')
	for study in study_list:
		study.cat = study.get_category_names()
	
	categories = Category.objects.filter(user=request.user)

	try: 
		timeline = Timeline.objects.get(owner=request.user)
		viewer_IDs = [ each.id for each in timeline.viewers.all()]
	except Timeline.DoesNotExist:
		viewer_IDs = []
	
	context = {
		'study_list' : study_list,
		'categories' : categories,
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

	same_user = request.user.pk == owner.pk
	has_permission = timeline.viewers.filter(id=request.user.id).exists()

	if (not same_user) and (not has_permission):
		return render(request, '403.html')

	study.cat = study.get_category_names()
	context = {
		'study' : study,
		'owner' : owner,
		'same_user' : same_user,
	}
	return render(request, 'timeline/detail.html', context)
