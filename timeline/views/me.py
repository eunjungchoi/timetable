from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from timeline.models import *


def me(request):
	user = request.user
	timeline = user.timeline_set.all()[0]
	viewer_IDs = [ each.id for each in timeline.viewers.all()]

	context = {
		'viewer_IDs' : viewer_IDs,
		}
	return render(request, 'timeline/me.html', context)
