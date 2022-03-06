from django.contrib import admin
from core import models

admin.site.register(models.Customer)
admin.site.register(models.Category)
admin.site.register(models.Job)
admin.site.register(models.Transactions)