from django.contrib import admin
from .models import User
from django.contrib.auth.models import Permission
# Register your models here.

admin.site.register(Permission)
admin.site.register(User)