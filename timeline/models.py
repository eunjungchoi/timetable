from django.db import models


class Study(models.Model):
	title = models.CharField(max_length=200)
	date = models.DateField()
	category = models.ManyToManyField('Category') 

	def __str__(self):
		return self.title


class Category(models.Model):
	name = models.CharField(max_length=30)
	
	def __str__(self):
			return self.name
