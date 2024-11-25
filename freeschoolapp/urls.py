from django.urls import path
from . import views

app_name='freeschoolapp'

#URLパターンを登録するためのリスト
urlpatterns=[
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
    path('clubpost',views.ClubPostView.as_view(),name='clubpost'),
    path('clubpostdone',views.ClubPostDoneView.as_view(),name='clubpostdone'),
    path('myclublist',views.MyClubListView.as_view(),name='myclublist'),
    path('myclubdetail',views.MyClubDetailView.as_view(),name='myclubdetail'),
    path('myclubupdate',views.MyClubUpDateView.as_view(),name='myclubupdate'),
    path('myclubdeletecheck',views.MyClubDeleteCheckView.as_view(),name='myclubdeletecheck'),
    path('myclubdeletedone',views.MyClubDeleteDoneView.as_view(),name='myclubdeletedone'),
    path('eventpost',views.EventPostView.as_view(),name='eventpost'),
    path('eventpostcheck',views.EventPostCheckView.as_view(),name='eventpostcheck'),
    path('eventpostdone',views.EventPostDoneView.as_view(),name='eventpostdone'),
    path('myeventlist',views.MyEventListView.as_view(),name='myeventlist'),
    path('myeventdetail',views.MyEventDetailView.as_view(),name='myeventdetail'),
    path('myeventupdate',views.MyEventUpDateView.as_view(),name='myeventupdate'),
    path('myeventdeletecheck',views.MyEventDeleteCheckView.as_view(),name='myeventdeletecheck'),
    path('myeventdeletedone',views.MyEventDeleteDoneView.as_view(),name='myeventdeletedone'),
    path('blogpost',views.BlogPostView.as_view(),name='blogpost'),
    path('blogpostcheck',views.BlogPostCheckView.as_view(),name='blogpostcheck'),
    path('mybloglist',views.MyBlogListView.as_view(),name='mybloglist'),
    path('myblogdetail',views.MyBlogDetailView.as_view(),name='myblogdetail'),
    path('myblogupdate',views.MyBlogUpDateView.as_view(),name='myblogupdate'),
    path('myblogdeletecheck',views.MyBlogDeleteCheckView.as_view(),name='myblogdeletecheck'),
    path('myblogdeletedone',views.MyBlogDeleteDoneView.as_view(),name='myblogdeletedone'),
    path('contact',views.ContactView.as_view(),name='contact'),
    path('contactdone',views.ContactDoneView.as_view(),name='contactdone')
]