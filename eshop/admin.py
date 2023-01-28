from django.contrib import admin
from .models import *
from django.apps import apps

# Register your models here.
admin.site.register(Product)
admin.site.register(Image)
admin.site.register(Category)

# all other models
models = apps.get_models()

for model in models:
    try:
        admin.site.register(model)
    except admin.sites.AlreadyRegistered:
        pass