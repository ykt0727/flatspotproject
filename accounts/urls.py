from django.urls import path
from . import views

app_name='accounts'

urlpatterns=[
    path('login',views.LoginView.as_view(),name='login'),
    path('student_signup',views.StudentSignupView.as_view(),name='student_signup'),
    path('student_signupdone',views.SignupDoneView.as_view(),name='student_signupdone')
]