from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    # ユーザー詳細画面のフィールドセットを定義
    fieldsets = (
        (None,{'fields':('login_id','password')}),
        ('Personal info',{'fields':('mail','phone_number','user_type')}),
        ('Important dates',{'fields':('last_login','date_joined')}),
        ('Permissions',{'fields':('is_staff','is_superuser','groups','user_permissions')}),
    )
    
    # ユーザー作成時のフィールドセットを定義
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("login_id", "mail", "phone_number", "user_type", "password1", "password2"),
            },
        ),
    )

    #管理画面で表示するフィールドを指定
    list_display=('login_id', 'user_type')
    #
    list_filter=()
    
    # リスト画面の並び順を指定
    ordering = ('login_id',)

    # 検索対象のフィールドを指定
    search_fields = ('login_id', 'mail')

admin.site.register(CustomUser, CustomUserAdmin)
