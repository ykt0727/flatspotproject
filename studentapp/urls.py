from django.urls import path
from . import views

app_name='studentapp'

#URLパターンを登録するためのリスト
urlpatterns=[path('',views.IndexView.as_view(),name='index')]