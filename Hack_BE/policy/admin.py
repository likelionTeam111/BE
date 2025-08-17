from django.contrib import admin
from .models import Policy, Favorite_policy

# Register your models here.
admin.site.register(Policy)
admin.site.register(Favorite_policy)