from django.contrib import admin

from .models import Study, Category, Timeline



class StudyAdmin(admin.ModelAdmin):
    list_display = ('date', 'title')

admin.site.register(Study, StudyAdmin)
admin.site.register(Category)
admin.site.register(Timeline)

