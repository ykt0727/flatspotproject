from django.contrib import admin

from .models import Student

#管理者サイトでの表示をカスタムできる
class StudentAdmin(admin.ModelAdmin):
    pass

#Django管理サイトにStudent,StudentAdminを登録する
admin.site.register(Student,StudentAdmin)
    