from django.contrib import admin

# Register your models here.

from user_app.models import CustomUserModel,UserProfileModel

admin.site.register(CustomUserModel)

admin.site.register(UserProfileModel)
