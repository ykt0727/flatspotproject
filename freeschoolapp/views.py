from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views import View
from .models import CustomUser,FreeSchool,Club,BlogPost
from .forms import ClubPostForm,BlogPostForm
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView
from django.urls import reverse_lazy

#ベースのビュー、ログイン中のユーザーの、FreeSchoolモデルに格納されている情報を取得する
class BaseView(View):
    
    #すべてのメソッドにログイン必須を適用
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        # ログイン済みで user_type が 'freeschool' であるか確認
        if not(self.request.user.is_authenticated and self.request.user.user_type=='freeschool'):
            # 条件を満たさない場合はアクセス拒否または別ページへリダイレクト
            return redirect('login')#ログインページや別のページにリダイレクト
        return super().dispatch(self.request,*args,**kwargs)
    #テンプレートに使用するコンテキスト情報を設定する
    def get_context_data(self, **kwargs):
        #contextを初期化
        context={}    
        if self.request.user.is_authenticated and self.request.user.user_type=='freeschool':
            #認証ユーザーに紐づいているFreeSchoolの行を取得
            freeschool=FreeSchool.objects.get(user=self.request.user)
            context['freeschool']=freeschool
        return context

class TopView(BaseView):
    #freeschool_top.htmlをレンダリング（描写）する
    def get(self, request, *args, **kwargs):
        #getリクエスト用の処理
        context=self.get_context_data(**kwargs)
        return render(request,'freeschool_top.html',context)
    def post(self, request, *args, **kwargs):
        #postリクエスト用の処理
        context=self.get_context_data(**kwargs)
        return render(request,'freeschool_top.html',context)

class MailSendView(TemplateView):
    
    #freeschool_passwordreset.htmlをレンダリング（描写）する
    template_name='freeschool_mailsend.html'
    

class MailSendDoneView(TemplateView):
    
    #freeschool_mailsenddone.htmlをレンダリング（描写）する
    template_name='freeschool_mailsenddone.html'


class AccountView(TemplateView):
    
    #freeschool_account.htmlをレンダリング（描写）する
    template_name='freeschool_account.html'


class AccountUpdateView(TemplateView):
    
    #freeschool_accountupdate.htmlをレンダリング（描写）する
    template_name='freeschool_accountupdate.html'


class PasswordResetView(TemplateView):
    
    #freeschool_passwordreset.htmlをレンダリング（描写）する
    template_name='freeschool_passwordreset.html'


class PasswordResetDoneView(TemplateView):
    
    #freeschool_passwordresetdone.htmlをレンダリング（描写）する
    template_name='freeschool_passwordresetdone.html'


class UserSearchView(TemplateView):
    
    #freeschool_usersearch.htmlをレンダリング（描写）する
    template_name='freeschool_usersearch.html'


class UserDetailView(TemplateView):
    
    #freeschool_userdetail.htmlをレンダリング（描写）する
    template_name='freeschool_userdetail.html'
    
    
class SessionTestView(TemplateView):
    
    #freeschool_sessiontest.htmlをレンダリング（描写）する
    template_name='freeschool_sessiontest.html'


class ClubPostView(BaseView,CreateView):

    #サークル掲載情報登録画面を表示
    template_name='freeschool_clubpost.html'
    #フォームとモデルを指定する
    form_class=ClubPostForm
    form=ClubPostForm
    model=Club
    
    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        #投稿フォームをcontextに格納
        context['clubpost_form']=self.form
        return context
    
    def form_valid(self,form):
        #POSTされたデータを取得
        postdata=form.save(commit=False)
        #ユーザー情報を設定
        postdata.user=self.request.user
        #保存
        postdata.save()
        
        return super().form_valid(form)
    
    def get_success_url(self):
        #成功後の遷移先URL
        return reverse_lazy('freeschoolapp:clubpostdone')
    #サークル掲載フォームを表示する処理
    # def get(self,request,*args,**kwargs):
        
    #     context=super().get_context_data(**kwargs)
    #     #Clubを作成するフォーム
    #     clubpost_form=ClubPostForm()
    #     context['clubpost_form']=clubpost_form
    #     #freeschool_clubpost.htmlにフォームをレンダリングする
    #     return render(request,'freeschool_clubpost.html',context)
    
    # def post(self,request,*args,**kwargs):
        
    #     context=super().get_context_data(**kwargs)
    #     #Clubを作成するフォーム
    #     clubpost_form=ClubPostForm()
    #     context['clubpost_form']=clubpost_form
    #     #freeschool_clubpost.htmlにフォームをレンダリングする
    #     return render(request,'freeschool_clubpost.html',context)
    

class ClubPostDoneView(TemplateView):
    
    #freeschool_clubpostdone.htmlをレンダリングする（描写）する
    template_name='freeschool_clubpostdone.html'

   
class MyClubListView(TemplateView):
    
    #freeschool_myclublist.htmlをレンダリング（描写）する
    template_name='freeschool_myclublist.html'
    

class MyClubDetailView(TemplateView):
    
    #freeschool_myclubdetail.htmlをレンダリング（描写）する
    template_name='freeschool_myclubdetail.html'
    
class MyClubUpDateView(TemplateView):
    
    #freeshool_myclubupdate.htmlをレンダリング（描写）する
    template_name='freeschool_myclubupdate.html'

class MyClubDeleteCheckView(TemplateView):
    
    #freeshool_myclubdeletecheck.htmlをレンダリング（描写）する
    template_name='freeschool_myclubdeletecheck.html'


class MyClubDeleteDoneView(TemplateView):
    
    #freeshool_myclubderetedoneview.htmlをレンダリング（描写）する
    template_name='freeschool_myclubdeletedone.html'

class EventPostView(TemplateView):
    
    #freeschool_eventpost.htmlをレンダリング（描写）する
    template_name='freeschool_eventpost.html'
    

class EventPostCheckView(TemplateView):
    
    #freshool_eventpostcheck.htmlをレンダリング（描写）する
    template_name='freeschool_eventpostcheck.html'


class EventPostDoneView(TemplateView):
    
    #freshool_eventpostdone.htmlをレンダリング（描写）する
    template_name='freeschool_eventpostdone.html'


class MyEventListView(TemplateView):
    
    #freeschool_myeventlist.htmlをレンダリング（描写）する
    template_name='freeschool_myeventlist.html'


class MyEventDetailView(TemplateView):
    
    #freeschool_myeventdetail.htmlをレンダリング（描写）する
    template_name='freeschool_myeventdetail.html'


class MyEventUpDateView(TemplateView):
    
    #freeschool_myeventupdate.htmlをレンダリング（描写）する
    template_name='freeschool_myeventupdate.html'


class MyEventDeleteCheckView(TemplateView):
    
    #freeschool_myeventdeleteCheck.htmlをレンダリング（描写）する
    template_name='freeschool_myeventdeletecheck.html'


class MyEventDeleteDoneView(TemplateView):
    
    #freeschool_myeventdeletedone.htmlをレンダリング（描写）する
    template_name='freeschool_myeventdeletedone.html'


class BlogPostView(BaseView,CreateView):
    #ブログ記事投稿画面を表示
    template_name='freeschool_blogpost.html'
    #フォームとモデルを指定する(必須)
    form_class=BlogPostForm
    form=BlogPostForm
    model=BlogPost
 
    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        #投稿フォームをcontextに格納
        context['post_form']=self.form
        return context
 
    def form_valid(self,form):
        #POSTされたデータを取得
        postdata=form.save(commit=False)
        # ユーザー情報を設定
        postdata.user=self.request.user
        #保存
        postdata.save()
       
        return super().form_valid(form)
 
    def get_success_url(self):
        # 成功後の遷移先URL
        return reverse_lazy('freeschoolapp:blogpost')
    

class BlogPostCheckView(TemplateView):
    
    #freeschool_blogpostcheck.htmlをレンダリング（描写）する
    template_name='freeschool_blogpostcheck.html'


class MyBlogListView(TemplateView):
    
    #freeschool_mybloglist.htmlをレンダリング（描写）する
    template_name='freeschool_mybloglist.html'
    
    
class MyBlogDetailView(TemplateView):
    
    #freeschool_myblogdetail.htmlをレンダリング（描写）する
    template_name='freeschool_myblogdetail.html'
    

class MyBlogUpDateView(TemplateView):
    
    #freeschool_myblogupdate.htmlをレンダリング（描写）する
    template_name='freeschool_myblogupdate.html'


class MyBlogDeleteCheckView(TemplateView):
    
    #freeschool_myblogdeletecheck.htmlをレンダリング（描写）する
    template_name='freeschool_myblogdeletecheck.html'
    
    
class MyBlogDeleteDoneView(TemplateView):
    
    #freeschool_myblogdeeltedone.htmlをレンダリング（描写）する
    template_name='freeschool_myblogdeletedone.html'


class ContactView(BaseView):
    #freeschool_contact.htmlをレンダリング(描写)する
    def get(self, request, *args, **kwargs):
        #getリクエスト用の処理
        context=self.get_context_data(**kwargs)
        return render(request,'freeschool_contact.html',context)
    def post(self, request, *args, **kwargs):
        #postリクエスト用の処理
        context=self.get_context_data(**kwargs)
        return render(request,'freeschool_contact.html',context)

class ContactDoneView(TemplateView):
    
    #freeschool_contactdone.htmlをレンダリング（描写）する
    template_name='freeschool_contactdone.html'

