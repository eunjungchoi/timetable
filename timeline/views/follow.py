from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404

from timeline.models import *


@login_required
def account(request, user_id):
	
	# try:
	# 	user = User.objects.get(pk=user_id)
	# except User.DoesNotExist:
	# 	return render(request, '404.html')

	# try:
	# 	timeline = Timeline.objects.get(owner=user)
	# except Timeline.DoesNotExist:
	# 	return render(request, '404.html')

	user = get_object_or_404(User, pk=user_id)
	timeline = get_object_or_404(Timeline, owner=user)

	same_user = request.user.pk == user.pk
	has_permission = timeline.followers.filter(id=request.user.id).exists()

	if (not same_user) and (not has_permission):
		return render(request, '403.html')

	study_list = Study.objects.filter(user=user).order_by('-date')
	for study in study_list:
		study.cat = [ each_cat.name for each_cat in study.category.all()]
	
	categories = Category.objects.filter(user=user)

	context = {
		'study_list' : study_list,
		'categories' : categories,
		'user' : request.user,
	}
	return render(request, 'timeline/index.html', context)


@login_required
def add_follower(request):
	timeline = get_object_or_404(Timeline, owner=request.user)

	# try:
	# 	timeline = Timeline.objects.get(owner=request.user)
	# except Timeline.DoesNotExist:
	# 	return render(request, '404.html')
		
	user = request.user
	follower_id = int(request.POST['follower_id_to_add'])

	try:
		follower = User.objects.get(pk=follower_id)
		if follower_id == request.user.id:
			pass
		elif not user.followings.filter(id=follower_id).exists():
			timeline.followers.add(follower)
	except: 
		pass

	return redirect(reverse('index'))


@login_required
def delete_follower(request):
	follower_id_list_to_del = request.POST.getlist('each_id_to_del')
	user = request.user
	timeline = Timeline.objects.get(owner=request.user)

	for each_id in follower_id_list_to_del:
		follower = User.objects.get(pk=int(each_id))
		timeline.followers.remove(follower)
		# timeline.followers = timeline.followers.exclude(id=follower.id)  << 이렇게 해도 동일한 결과

		# each_follower = timeline.followers.get(id=int(each_id))
		# each_follower.delete()  
		# : 이렇게 하면 user 인스턴스가 통째로 삭제됨. 본의 아니게 남의 계정을 삭제하는 부작용
	
	return redirect(reverse('index'))

