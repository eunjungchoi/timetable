from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import JsonResponse

from timeline.models import *


@login_required
def add(request):
	json = {}

	if not request.POST['name']:
		return JsonResponse(json, status=405)

	cat_name = request.POST['name'].strip()

	if request.user.category_set.filter(name=cat_name).exists():
		json["message"] = "동일한 카테고리가 있습니다"
		return JsonResponse(json, status=400)

	else:
		c = Category.objects.create(
			user=request.user,
			name=cat_name,
		)
		json["name"] = cat_name
		json["id"] = c.id

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
