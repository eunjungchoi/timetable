from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from timeline.models import *


@login_required
def add(request):
	c, created = Category.objects.get_or_create(
		user=request.user, 
		name=request.POST['name'],
	)

	return redirect(reverse('index'))


@login_required
def delete(request):
	cat_id_list_to_del = request.POST.getlist('cat_name')
	
	for cat_id in cat_id_list_to_del:
		each = Category.objects.filter(user=request.user).get(id=cat_id)
		each.delete()

	return redirect(reverse('index'))