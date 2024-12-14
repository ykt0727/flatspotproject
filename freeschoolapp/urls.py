from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name='freeschoolapp'

#URLパターンを登録するためのリスト
urlpatterns=[
    path('top',views.TopView.as_view(),name='top'),
    path('account',views.AccountView.as_view(),name='account'),
    path('accountupdate',views.AccountUpdateView.as_view(),name='accountupdate'),
    #マイページ機能
    path('mypage',views.MypageView.as_view(),name='mypage'),#アカウント情報表示
    path('mypageupdate',views.MypageUpdateView.as_view(),name='mypageupdate'),#アカウント情報変更
    #ユーザー検索画面(閲覧権限)
    path('usersearch',views.UserSearchView.as_view(),name='usersearch'),
    path('userdetail/<int:pk>/',views.UserDetailView.as_view(),name='userdetail'),
    #サークル機能
    path('clubpost',views.ClubPostView.as_view(),name='clubpost'),
    path('clubpostdone',views.ClubPostDoneView.as_view(),name='clubpostdone'),
    path('myclublist',views.MyClubListView.as_view(),name='myclublist'),
    path('myclubdetail/<int:pk>',views.MyClubDetailView.as_view(),name='myclubdetail'),
    path('myclubupdate/<int:pk>',views.MyClubUpDateView.as_view(),name='myclubupdate'),
    path('myclubdeletecheck/<int:pk>',views.MyClubDeleteCheckView.as_view(),name='myclubdeletecheck'),
    path('myclubdeletedone',views.MyClubDeleteDoneView.as_view(),name='myclubdeletedone'),
    #イベント機能
    path('eventpost',views.EventPostView.as_view(),name='eventpost'),
    path('eventpostdone',views.EventPostDoneView.as_view(),name='eventpostdone'),
    path('myeventlist',views.MyEventListView.as_view(),name='myeventlist'),
    path('myeventdetail/<int:pk>',views.MyEventDetailView.as_view(),name='myeventdetail'),
    path('myeventupdate/<int:pk>',views.MyEventUpDateView.as_view(),name='myeventupdate'),
    path('myeventdeletecheck/<int:pk>',views.MyEventDeleteCheckView.as_view(),name='myeventdeletecheck'),
    path('myeventdeletedone',views.MyEventDeleteDoneView.as_view(),name='myeventdeletedone'),
    #ブログ機能
    path('blogpost',views.BlogPostView.as_view(),name='blogpost'),
    path('blogpostcheck',views.BlogPostCheckView.as_view(),name='blogpostcheck'),
    path('mybloglist',views.MyBlogListView.as_view(),name='mybloglist'),
    path('myblogdetail',views.MyBlogDetailView.as_view(),name='myblogdetail'),
    path('myblogupdate',views.MyBlogUpDateView.as_view(),name='myblogupdate'),
    path('myblogdeletecheck',views.MyBlogDeleteCheckView.as_view(),name='myblogdeletecheck'),
    path('myblogdeletedone',views.MyBlogDeleteDoneView.as_view(),name='myblogdeletedone'),
    #お問い合わせ機能
    path('contact',views.ContactView.as_view(),name='contact'),
    path('contactdone',views.ContactDoneView.as_view(),name='contactdone')
]
