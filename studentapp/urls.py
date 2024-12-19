from django.urls import path
from . import views

app_name='studentapp'

#URLパターンを登録するためのリスト
urlpatterns=[
    path('top',views.TopView.as_view(),name='top'),
    #サークル機能
    path('clublist',views.ClubListView.as_view(),name='clublist'),
    path('clubdetail/<int:pk>',views.ClubDetailView.as_view(),name='clubdetail'),
    path('clubrequest/<int:club_id>/',views.ClubRequestView.as_view(),name='clubrequest'),
    path('clubrequestdone',views.ClubRequestDoneView.as_view(),name='clubrequestdone'),
            #いいね機能
    path('clublike/<int:pk>',views.LikeForClubView.as_view(), name='clublike'),
    
    #イベント機能
    path('eventlist',views.EventListView.as_view(),name='eventlist'),
    path('eventdetail/<int:pk>',views.EventDetailView.as_view(),name='eventdetail'),
    path('eventrequest/<int:event_id>/',views.EventRequestView.as_view(),name='eventrequest'),
    path('eventrequestdone',views.EventRequestDoneView.as_view(),name='eventrequestdone'),
            #いいね機能
    path('eventlike/<int:pk>',views.LikeForEventView.as_view(), name='eventlike'),
    
    #ブログ機能
    path('bloglist',views.BlogListView.as_view(),name='bloglist'),
    path('blogdetail/<int:pk>',views.BlogDetailView.as_view(),name='blogdetail'),
        #いいね機能
    path('blogpostlike/<int:pk>',views.LikeForBlogView.as_view(), name='blogpostlike'),
    
    #お問い合わせ機能
    path('contact',views.ContactView.as_view(),name='contact'),
    path('contactdone',views.ContactDoneView.as_view(),name='contactdone'),
    
    #このサイトについて
    path('about',views.AboutView.as_view(),name='about'),
    
    #マイページ機能
    path('mypage',views.MypageView.as_view(),name='mypage'),#アカウント情報表示
    path('mypageupdate',views.MypageUpdateView.as_view(),name='mypageupdate'),#アカウント情報変更
    path('mypagedeletecheck',views.MypageDeleteCheckView.as_view(),name='mypagedeletecheck'),#アカウント情報削除確認画面
    path('accountdelete',views.AccountDeleteView.as_view(),name='accountdelete'),#アカウントを削除する処理
    path('mypagedeletedone',views.MypageDeleteDoneView.as_view(),name='mypagedeletedone')#アカウント削除完了画面
]    
