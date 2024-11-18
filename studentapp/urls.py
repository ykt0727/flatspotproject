from django.urls import path
from . import views

app_name='studentapp'

#URLパターンを登録するためのリスト
urlpatterns=[
    path('top',views.TopView.as_view(),name='top'),
    path('clublist',views.ClubListView.as_view(),name='clublist'),
    path('clubdetail',views.ClubDetailView.as_view(),name='clubdetail'),
    path('clubrequest',views.ClubRequestView.as_view(),name='clubrequest'),
    path('clubrequestdone',views.ClubRequestDoneView.as_view(),name='clubrequestdone'),
    path('eventlist',views.EventListView.as_view(),name='eventlist'),
    path('eventdetail',views.EventDetailView.as_view(),name='eventdetail'),
    path('eventrequest',views.EventRequestView.as_view(),name='eventrequest'),
    path('eventrequestdone',views.EventRequestDoneView.as_view(),name='eventrequestdone'),
    path('bloglist',views.BlogListView.as_view(),name='bloglist'),
    path('blogdetail',views.BlogDetailView.as_view(),name='blogdetail'),
    path('contact',views.ContactView.as_view(),name='contact'),
    path('contactdone',views.ContactDoneView.as_view(),name='contactdone'),
    path('about',views.AboutView.as_view(),name='about'),
    ]