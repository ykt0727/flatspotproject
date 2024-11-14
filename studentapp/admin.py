from django.contrib import admin
from .models import StudentUser

#Django管理者サイトにStudentUserを登録する
admin.site.register(StudentUser)