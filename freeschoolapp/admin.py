from django.contrib import admin

from .models import FreeSchool 

#管理サイトでの表示をカスタムする
class FreeSchoolAdmin(admin.ModelAdmin):
    pass

#管理サイトにFreeSchoolとFreeSchooladminを追加する
admin.site.register(FreeSchool,FreeSchoolAdmin)

