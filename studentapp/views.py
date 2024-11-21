from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views import View
from .models import Student

#ベースのビュー、ログイン中のユーザーの、FreeSchoolモデルに格納されている情報を取得する
class BaseView(View):
    #テンプレートに使用するコンテキスト情報を設定する
    def get_context_data(self, **kwargs):
        #contextを初期化
        context={}    
        if self.request.user.is_authenticated and self.request.user.user_type=='student':
            #認証ユーザーに紐づいているStudentの行を取得
            student=Student.objects.get(user=self.request.user)
            context['student']=student
        return context

class TopView(BaseView):
    #student_top.htmlをレンダリング（描写）する
    def get(self, request, *args,**kwargs):
        #getリクエスト用の処理
        context=self.get_context_data(**kwargs)
        return render(request,'student_top.html',context)
    def post(self, request, *args,**kwargs):
        #postリクエスト用の処理
        context=self.get_context_data(**kwargs)
        return render(request,'student_top.html',context)
    

class ClubListView(BaseView):
    #student_clublist.htmlをレンダリング（描写）する
    def get(self, request, *args,**kwargs):
        #getリクエスト用の処理
        context=self.get_context_data(**kwargs)
        return render(request,'student_clublist.html',context)
    def post(self, request, *args,**kwargs):
        #postリクエスト用の処理
        context=self.get_context_data(**kwargs)
        return render(request,'student_clublist.html',context)
    
class ClubDetailView(BaseView):
    #student_clubdetail.htmlをレンダリング（描写）する
    def get(self, request, *args,**kwargs):
        #getリクエスト用の処理
        context=self.get_context_data(**kwargs)
        return render(request,'student_clubdetail.html',context)
    def post(self, request, *args,**kwargs):
        #postリクエスト用の処理
        context=self.get_context_data(**kwargs)
        return render(request,'student_cluvdetail.html',context)

class ClubRequestView(BaseView):
    #student_clubrequest.htmlをレンダリング（描写）する
    def get(self, request, *args,**kwargs):
        #getリクエスト用の処理
        context=self.get_context_data(**kwargs)
        return render(request,'student_clubrequest.html',context)
    def post(self, request, *args,**kwargs):
        #postリクエスト用の処理
        context=self.get_context_data(**kwargs)
        return render(request,'student_clubrequest.html',context)
    
    
class ClubRequestDoneView(BaseView):
    #student_clubrequestdone.htmlをレンダリング（描写）する
    def get(self, request, *args,**kwargs):
        #getリクエスト用の処理
        context=self.get_context_data(**kwargs)
        return render(request,'student_clubrequestdone.html',context)
    def post(self, request, *args,**kwargs):
        #postリクエスト用の処理
        context=self.get_context_data(**kwargs)
        return render(request,'student_clubrequestdone.html',context)
class EventListView(BaseView):
    #student_eventlist.htmlをレンダリング（描写）する
    def get(self, request, *args,**kwargs):
        #getリクエスト用の処理
        context=self.get_context_data(**kwargs)
        return render(request,'student_eventlist.html',context)
    def post(self, request, *args,**kwargs):
        #postリクエスト用の処理
        context=self.get_context_data(**kwargs)
        return render(request,'student_eventlist.html',context)

class EventDetailView(BaseView):
    #student_eventdetail.htmlをレンダリング（描写）する
    def get(self, request, *args,**kwargs):
        #getリクエスト用の処理
        context=self.get_context_data(**kwargs)
        return render(request,'student_eventdetail.html',context)
    def post(self, request, *args,**kwargs):
        #postリクエスト用の処理
        context=self.get_context_data(**kwargs)
        return render(request,'student_eventdetail.html',context)

class EventRequestView(BaseView):
    #student_eventrequest.htmlをレンダリング（描写）する
    def get(self, request, *args,**kwargs):
        #getリクエスト用の処理
        context=self.get_context_data(**kwargs)
        return render(request,'student_eventrequest.html',context)
    def post(self, request, *args,**kwargs):
        #postリクエスト用の処理
        context=self.get_context_data(**kwargs)
        return render(request,'student_eventrequest.html',context)    
    
class EventRequestDoneView(BaseView):
    #student_eventrequestdone.htmlをレンダリング（描写）する
    def get(self, request, *args,**kwargs):
        #getリクエスト用の処理
        context=self.get_context_data(**kwargs)
        return render(request,'student_eventrequestdone.html',context)
    def post(self, request, *args,**kwargs):
        #postリクエスト用の処理
        context=self.get_context_data(**kwargs)
        return render(request,'student_eventrequestdone.html',context)

class BlogListView(BaseView):
    #student_bloglist.htmlをレンダリング（描写）する
    def get(self, request, *args,**kwargs):
        #getリクエスト用の処理
        context=self.get_context_data(**kwargs)
        return render(request,'student_bloglist.html',context)
    def post(self, request, *args,**kwargs):
        #postリクエスト用の処理
        context=self.get_context_data(**kwargs)
        return render(request,'student_bloglist.html',context)

class BlogDetailView(BaseView):
    #student_blogdetail.htmlをレンダリング（描写）する
    def get(self, request, *args,**kwargs):
        #getリクエスト用の処理
        context=self.get_context_data(**kwargs)
        return render(request,'student_blogdetail.html',context)
    def post(self, request, *args,**kwargs):
        #postリクエスト用の処理
        context=self.get_context_data(**kwargs)
        return render(request,'student_blogdetail.html',context)

class ContactView(BaseView):
    #student_contact.htmlをレンダリング（描写）する
    def get(self, request, *args,**kwargs):
        #getリクエスト用の処理
        context=self.get_context_data(**kwargs)
        return render(request,'student_contact.html',context)
    def post(self, request, *args,**kwargs):
        #postリクエスト用の処理
        context=self.get_context_data(**kwargs)
        return render(request,'student_contact.html',context)    

class ContactDoneView(TemplateView):
    #student_contactdone.htmlをレンダリング（描写）する
    def get(self, request, *args,**kwargs):
        #getリクエスト用の処理
        context=self.get_context_data(**kwargs)
        return render(request,'student_contactdone.html',context)
    def post(self, request, *args,**kwargs):
        #postリクエスト用の処理
        context=self.get_context_data(**kwargs)
        return render(request,'student_contactdone.html',context)

class AboutView(TemplateView):
    #student_about.htmlをレンダリング（描写）する
    def get(self, request, *args,**kwargs):
        #getリクエスト用の処理
        context=self.get_context_data(**kwargs)
        return render(request,'student_about.html',context)
    def post(self, request, *args,**kwargs):
        #postリクエスト用の処理
        context=self.get_context_data(**kwargs)
        return render(request,'student_about.html',context)