from django.contrib import admin
from .models import FreeSchoolUser

#Django管理者サイトにFreeSchoolUserを登録する
admin.site.register(FreeSchoolUser)