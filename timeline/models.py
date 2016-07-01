from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

class Study(models.Model):
	user = models.ForeignKey(User)
	timeline = models.ForeignKey('Timeline', null=True, blank=True, default = None)
	title = models.CharField(max_length=100)
	date = models.DateField()
	contents = models.TextField(max_length=500)
	category = models.ManyToManyField('Category')


	def __str__(self):
		return self.title

	def get_category_names(self):
		return [ each_cat.name for each_cat in self.category.all()]

# for test:
	def has_category(self, category_id):
		return False


class Category(models.Model):
	user = models.ForeignKey(User)
	timeline = models.ForeignKey('Timeline', null=True, blank=True, default = None)
	name = models.CharField(max_length=30)

	
	def __str__(self):
			return self.name


class Timeline(models.Model):
	owner = models.ForeignKey(User)
	followers = models.ManyToManyField(User, related_name ='followings')


#################
# 풀어서 쓰면, 이런 느낌.
# 
# class Audience(models.Model):
# 	user = models.ForeignKey(User, related_name='owner')
# 
# class Audience_Audience(Models.Model)	
# 	audience = models.ForeignKey(Audience)
# 	user = models.ForeignKey(User)

# ...
# 같은 테이블에 대한 ManyToMany
# class ViewPermission(Models.Model)	
# 	user = models.ForeignKey(User)
# 	viewer = models.ForeignKey(User)

def create_user_default_timeline(sender, instance, created, **kwargs):
    if created:
        Timeline.objects.create(owner=instance)

post_save.connect(create_user_default_timeline, sender=User)
