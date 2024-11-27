from django.shortcuts import render,get_object_or_404
from django.views.generic import TemplateView,ListView,DetailView,FormView
from django.urls import reverse_lazy
from django.views import View

#モデル、フォーム関連
from .models import Student
from .forms import ClubRequestForm

from freeschoolapp.models import BlogPost,Club
from django.core.mail import EmailMessage

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
    

class ClubListView(ListView):
    #student_clublist.htmlをレンダリング（描写）する
    template_name=('student_clublist.html')
    #モデルを指定
    model=Club
    #モデルBlogPostのオブジェクトにquerysetを適用
    queryset=Club.objects.order_by('created_at')
    #1ページに表示するレコードの件数を設定
    paginate_by=5
    
class ClubDetailView(DetailView):
    template_name='student_clubdetail.html'
    #モデルを設定
    model=Club

class ClubRequestView(FormView):
    
    #student_clubrequest.htmlをレンダリング（描写）する
    template_name="student_clubrequest.html"
    #クラス変数form_classに設定
    form_class=ClubRequestForm
    #送信完了後遷移する
    success_url=reverse_lazy('studentapp:clubrequestdone')
    
    def get_initial(self):
        #初期値の取得
        initial=super().get_initial()
        
        #URLのパラメータからclub_idを取得
        club_id=self.kwargs.get('club_id') 
        
        #フォームに club_id を渡す
        initial['club_id']=club_id
        
        return initial
    
    #フォームのバリデーションを通過したデータがPOSTされたときに呼ばれるメール送信を行う
    def form_valid(self,form):
        
        #URLのパラメータからclub_idを取得
        club_id=self.kwargs.get('club_id')        
        #Clubオブジェクトを取得
        club=get_object_or_404(Club,pk=club_id)
        
        sender_email=self.request.user.email
        club_owner_email=club.email
        message=form.cleaned_data['message']
        
        # メールの内容をビューで動的に設定
        subject='サークルに体験申請が来ました！'
        body=f'<h1>新しい体験申請がありました！</h1>'
        body+=f'<p><strong>申請者のメールアドレス:</strong> {sender_email}</p>'
        body+=f'<p><strong>メッセージ:</strong></p><p>{message}</p>'
        
        # メール送信
        email=EmailMessage(
            #タイトル
            subject=subject,
            #本文
            body=body,
            #送信元
            from_email=sender_email,
            #宛先
            to=[club_owner_email],
            #HTMLメールとして送信
            headers={'Content-Type':'text/html'},  
        )
        email.send()
        
        return super().form_valid(form)
    
class ClubRequestDoneView(TemplateView):
    #student_clubrequestdone.htmlをレンダリング（描写）する 
    template_name="student_clubrequestdone.html"
    
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

#ブログ記事一覧
class BlogListView(ListView):
    #student_bloglist.htmlをレンダリング（描写）する
    template_name=('student_bloglist.html')
    #モデルを指定
    model=BlogPost
    #モデルBlogPostのオブジェクトにquerysetを適用
    queryset=BlogPost.objects.order_by('created_at')
    
    #1ページに表示するレコードの件数を設定
    paginate_by=5
    

class BlogDetailView(DetailView):
    #student_blogdetail.htmlをレンダリング（描写）する
    template_name='blogdetail.html'
    #モデルを設定
    model=BlogPost

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