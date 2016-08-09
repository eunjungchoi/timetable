from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.utils import timezone
from social.apps.django_app.default.models import UserSocialAuth


def get_profile_image(self):
	try:
		social = self.social_auth.get()
		url = 'https://graph.facebook.com/{0}/picture'.format(social.uid)
	except UserSocialAuth.DoesNotExist:
		url = ''
	return url

User.add_to_class("get_profile_image", get_profile_image)


def user_directory_path(instance, filename):
    return 'timeline/{0}_{1}_{2}'.format(instance.user.id, int(timezone.now().timestamp()), filename)


class Study(models.Model):
	title = models.CharField(max_length=100)
	contents = models.TextField(max_length=500)
	date = models.DateField()
	pic = models.ImageField(upload_to=user_directory_path, null=True, blank=True, default=None)

	user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="studies")
	timeline = models.ForeignKey('Timeline', null=True, blank=True, default = None)
	category = models.ManyToManyField('Category')

	created_at = models.DateTimeField(null=True, default=None)
	updated_at = models.DateTimeField(null=True, default=None)


	@staticmethod
	def calculate_image_dimension(width, height, max_size=(720, 720)):
		max_width, max_height = max_size

		image_ratio = width / float(height)

		if width < max_width and height < max_height:
			new_width = width
			new_height = height
		elif width > height:
			new_width = max_width
			new_height = new_width / image_ratio
		else:
			new_height = max_height
			new_width  = new_height * image_ratio

		return int(new_width), int(new_height)


	def resize_image(self, max_size):
		from PIL import Image
		import io
		import os
		from django.core.files.uploadedfile import SimpleUploadedFile

		image = Image.open(self.pic)
		image_width, image_height = image.size
		new_width, new_height = Study.calculate_image_dimension(image_width, image_height, max_size)

		resized_image = image.resize((new_width, new_height), Image.ANTIALIAS)

		tempfile_io = io.BytesIO()
		resized_image.save(tempfile_io, format=image.format)

		self.pic = SimpleUploadedFile(name=self.pic.name, content=tempfile_io.getvalue(), content_type='image/jpeg')

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


class LatestStudy(Study):
	class Meta:
		ordering = ["-date", "-created_at"]
		proxy = True



class Category(models.Model):
	name = models.CharField(max_length=30)

	user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
	timeline = models.ForeignKey('Timeline', null=True, blank=True, default = None)

	def __str__(self):
			return self.name


class Timeline(models.Model):
	owner = models.ForeignKey(User, on_delete=models.DO_NOTHING)
	viewers = models.ManyToManyField(User, related_name ='viewers')

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
