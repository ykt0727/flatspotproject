from django.urls import path
from . import views

app_name='freeschoolapp'

#URLパターンを登録するためのリスト
urlpatterns=[
    path('login',views.LoginView.as_view(),name='login'),
    path('top',views.TopView.as_view(),name='top'),
    path('mailsend',views.MailSendView.as_view(),name='mailsend'),
    path('mailsenddone',views.MailSendDoneView.as_view(),name='mailsenddone'),
    path('account',views.AccountView.as_view(),name='account'),
    path('accountupdate',views.AccountUpdateView.as_view(),name='accountupdate'),
    path('passwordreset',views.PasswordResetView.as_view(),name='passwordreset'),
    path('passwordresetdone',views.PasswordResetDoneView.as_view(),name='passwordresetdone'),
    path('usersearch',views.UserSearchView.as_view(),name='usersearch'),
    path('userdetail',views.UserDetailView.as_view(),name='userdetail'),
    path('sessiontest',views.SessionTestView.as_view(),name='sessiontest'),
    path('mybloglist',views.MyBlogListView.as_view(),name='mybloglist'),
]