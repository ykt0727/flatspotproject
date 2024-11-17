from django.shortcuts import render
from django.views.generic.base import TemplateView

#仮でTemplateViewを継承してlogin.htmlを描画する
class LoginView(TemplateView):
    template_name='login.html'