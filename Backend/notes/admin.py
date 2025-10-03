from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.UploadedFile)
admin.site.register(models.Summary)
admin.site.register(models.Quiz)
admin.site.register(models.CommonBook)
