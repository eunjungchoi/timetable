from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import JsonResponse

from timeline.models import *


@login_required
def add(request):
	json = {
		'result': 'error',
	}

	if not request.POST['cat_name_to_add']:
		return JsonResponse(json)

	cat_name = request.POST['cat_name_to_add']

	try:
		c = Category.objects.get(
			name=cat_name,
		)
		json["cat_name_to_add"] = cat_name
	except Category.DoesNotExist:
		c = Category.objects.create(
			user=request.user,
			name=cat_name,
		)
		json["result"] = "success"
		json["cat_name_to_add"] = cat_name

	return JsonResponse(json)



@login_required
def delete(request):
	json = {
		'result': 'error',
	}

	if not request.POST.getlist('cat_id_to_del'):
		return JsonResponse(json)

	cat_id_list_to_del = request.POST.getlist('cat_id_to_del')

	for cat_id in cat_id_list_to_del:
		each = Category.objects.filter(user=request.user).get(id=int(cat_id))
		each.delete()
		json["result"] = "success"
		json["cat_id_list_to_del"] = cat_id_list_to_del

	return JsonResponse(json)
