from django.urls import path
from . import views

app_name='accounts'

urlpatterns=[
    path('student_signup',views.StudentSignupView.as_view(),name='student_signup'),
    path('student_signupdone',views.StudentSignupDoneView.as_view(),name='student_signupdone'),
    path('login',views.CustomLoginView.as_view(),name='login'),
]
