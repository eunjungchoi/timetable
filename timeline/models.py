from django.db import models

# Create your models here.


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



# cat02 = models.BooleanField()
	# cat03 = models.BooleanField()
	# cat04 = models.BooleanField()
	# cat05 = models.BooleanField()
	# cat06 = models.BooleanField()
	# cat07 = models.BooleanField()
	# cat08 = models.BooleanField()
	# cat09 = models.BooleanField()
	# cat10 = models.BooleanField()

	# name02 = models.CharField(max_length=30)
	# name03 = models.CharField(max_length=30)
	# name04 = models.CharField(max_length=30)
	# name05 = models.CharField(max_length=30)
	# name06 = models.CharField(max_length=30)
	# name07 = models.CharField(max_length=30)
	# name08 = models.CharField(max_length=30)
	# name09 = models.CharField(max_length=30)
	# name10 = models.CharField(max_length=30)
