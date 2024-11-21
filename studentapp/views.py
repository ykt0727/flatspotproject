from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views import View

#ベースのビュー、ログイン中のユーザーの、FreeSchoolモデルに格納されている情報を取得する
class BaseView(View):
    #テンプレートに使用するコンテキスト情報を設定する
    def get_context_data(self, **kwargs):
        #contextを初期化
        context={}    
        if self.request.user.is_authenticated and self.request.user.user_type=='student':
            #認証ユーザーに紐づいているStudentの行を取得
            student=student.objects.get(user=self.request.user)
            context['student']=student
        return context

class TopView(TemplateView):
    
    #student_top.htmlをレンダリング（描写）する
    template_name='student_top.html'
    

class ClubListView(TemplateView):
    
    #student_clublist.htmlをレンダリング（描写）する
    template_name='student_clublist.html'
    
    
class ClubDetailView(TemplateView):
    
    #student_clubdetail.htmlをレンダリング（描写）する
    template_name='student_clubdetail.html'


class ClubRequestView(TemplateView):
    
    #student_clubrequest.htmlをレンダリング（描写）する
    template_name='student_clubrequest.html'
    
    
class ClubRequestDoneView(TemplateView):
    
    #student_clubrequestdone.htmlをレンダリング（描写）する
    template_name='student_clubrequestdone.html'


class EventListView(TemplateView):
    
    #student_eventlist.htmlをレンダリング（描写）する
    template_name='student_eventlist.html'


class EventDetailView(TemplateView):
    
    #student_eventdetail.htmlをレンダリング（描写）する
    template_name='student_eventdetail.html'


class EventRequestView(TemplateView):
    
    #student_eventrequest.htmlをレンダリング（描写）する
    template_name='student_eventrequest.html'
    
    
class EventRequestDoneView(TemplateView):
    
    #student_eventrequestdone.htmlをレンダリング（描写）する
    template_name='student_eventrequestdone.html'


class BlogListView(TemplateView):
    
    #student_bloglist.htmlをレンダリング（描写）する
    template_name='student_bloglist.html'


class BlogDetailView(TemplateView):
    
    #student_blogdetail.htmlをレンダリング（描写）する
    template_name='student_blogdetail.html'


class ContactView(TemplateView):
    
    #student_contact.htmlをレンダリング（描写）する
    template_name='student_contact.html'


class ContactDoneView(TemplateView):
    
    #student_contactdone.htmlをレンダリング（描写）する
    template_name='student_contactdone.html'


class AboutView(TemplateView):
    
    #student_about.htmlをレンダリング（描写）する
    template_name='student_about.html'