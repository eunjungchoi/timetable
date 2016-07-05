from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.utils import timezone


class Study(models.Model):
	title = models.CharField(max_length=100)
	contents = models.TextField(max_length=500)
	date = models.DateField()

	user = models.ForeignKey(User)
	timeline = models.ForeignKey('Timeline', null=True, blank=True, default = None)
	category = models.ManyToManyField('Category')

	created_at = models.DateTimeField(null=True, default=None)
	updated_at = models.DateTimeField(null=True, default=None)


	def save(self, *args, **kwargs):
		if not self.id:
			self.created_at = timezone.now()
		self.updated_at = timezone.now()

		return super(Study, self).save(*args, **kwargs)


	def __str__(self):
		return self.title

	def get_category_names(self):
		return [ each_cat.name for each_cat in self.category.all()]

# for test:
	def has_category(self, category_id):
		return False


class Category(models.Model):
	name = models.CharField(max_length=30)

	user = models.ForeignKey(User)
	timeline = models.ForeignKey('Timeline', null=True, blank=True, default = None)
	
	def __str__(self):
			return self.name


class Timeline(models.Model):
	owner = models.ForeignKey(User)
	followers = models.ManyToManyField(User, related_name ='followings')

	def __str__(self):
		return self.owner.username


def create_user_default_timeline(sender, instance, created, **kwargs):
    if created:
        Timeline.objects.create(owner=instance)



#################
# class Timeline >> 풀어서 쓰면,
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



post_save.connect(create_user_default_timeline, sender=User)
