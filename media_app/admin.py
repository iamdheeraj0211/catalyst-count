from django.contrib import admin
from .models import *
# Register your models here.

class UploadAdmin(admin.ModelAdmin):
    list_display = ['id','document','created_at','created_by']

admin.site.register(UploadDataModel,UploadAdmin)