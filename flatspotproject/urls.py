"""
URL configuration for flatspotproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    
    #studentアプリのURLを登録する
    path('student/',include('studentapp.urls')),
    #freeschoolアプリのURLを登録する
    path('freeschool/',include('freeschoolapp.urls')),
    #accountsアプリのURLを登録する
    path('accounts/',include('accounts.urls')),
    
    #パスワードリセット関連の登録
    path('password_reset',auth_views.PasswordResetView.as_view(template_name='passwordreset.html'),name='password_reset'),
    path('password_reset/done',auth_views.PasswordResetDoneView.as_view(template_name='passwordresetsent.html'),name='password_reset_done'),
    path('reset/<uidb64>/<token>',auth_views.PasswordResetConfirmView.as_view(template_name='passwordresetform.html'),name='password_reset_confirm'),
    path('reset/done',auth_views.PasswordResetCompleteView.as_view(template_name='passwordresetdone.html'),name='password_reset_complete'),
    
]
#mediaフォルダのURLを追加、開発環境では必要
urlpatterns+=static(
    #MEDIA_URLはmedia/
    settings.MEDIA_URL,
    #MEDIA_ROOTにはmediaフォルダのパスが入っている
    document_root=settings.MEDIA_ROOT)
