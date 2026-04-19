from django.contrib import admin
from .models import Subject, StudyGroup, Membership, Category

admin.site.register(Subject)
admin.site.register(StudyGroup)
admin.site.register(Membership)
admin.site.register(Category)     
