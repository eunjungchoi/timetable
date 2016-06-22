from django.db import models
from django.contrib.auth.models import User

class Study(models.Model):
	user = models.ForeignKey(User)
	title = models.CharField(max_length=100)
	date = models.DateField()
	contents = models.TextField(max_length=500)
	category = models.ManyToManyField('Category') 

	def __str__(self):
		return self.title


class Category(models.Model):
	user = models.ForeignKey(User)
	name = models.CharField(max_length=30)
	
	def __str__(self):
			return self.name


