from django.contrib import admin

from .models import CustomUser

class CustomUserAdmin(admin.ModelAdmin):
    pass


#Django管理サイトにCCustomUser,CustomUserAdminを登録する

admin.site.register(CustomUser,CustomUserAdmin)