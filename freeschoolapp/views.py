from django.shortcuts import render
from django.views.generic.base import TemplateView

class IndexView(TemplateView):
    
    #index.htmlをレンダリング（描写）する
    template_name='freeschool_login.html'