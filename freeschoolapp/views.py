from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views import View
from .models import CustomUser,FreeSchool,Club,Event,BlogPost
from .forms import ClubPostForm,EventPostForm,BlogPostForm
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView,ListView,DetailView,UpdateView,DeleteView
from django.urls import reverse_lazy
from studentapp.models import Student

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


class AccountView(TemplateView):
    
    #freeschool_account.htmlをレンダリング（描写）する
    template_name='freeschool_account.html'


class AccountUpdateView(TemplateView):
    
    #freeschool_accountupdate.htmlをレンダリング（描写）する
    template_name='freeschool_accountupdate.html'


class UserSearchView(ListView):
    
    #freeschool_usersearch.htmlをレンダリング（描写）する
    template_name='freeschool_usersearch.html'
    
    #1ページに表示する件数
    paginate_by=10
    
    #モデルを指定する
    model=Student
    
    def get_queryset(self, **kwargs):
        queryset=super().get_queryset(**kwargs)
        query=self.request.GET.get('q','')

        if query!='':
            queryset=queryset.filter(nickname=query)

        return queryset.order_by('-id')


class UserDetailView(UpdateView):
    
    #freeschool_userdetail.htmlをレンダリング（描写）する
    template_name='freeschool_userdetail.html'

    #モデルを指定する
    model=Student
    
    #フィールドを指定する
    fields=('is_view',)
    
    success_url=reverse_lazy('freeschoolapp:usersearch')

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
    

class ClubPostDoneView(TemplateView):
    
    #freeschool_clubpostdone.htmlをレンダリングする（描写）する
    template_name='freeschool_clubpostdone.html'

   
class MyClubListView(ListView):
    
    #freeschool_myclublist.htmlをレンダリング（描写）する
    template_name='freeschool_myclublist.html'
    
    #投稿されたサークルを投稿日時の降順（新しい順）に並べ替える
    queryset=Club.objects.order_by('-created_at')
    
    #1ページに表示する件数
    paginate_by=10
    

class MyClubDetailView(DetailView):
    
    #freeschool_myclubdetail.htmlをレンダリング（描写）する
    template_name='freeschool_myclubdetail.html'
    
    #モデルを指定する
    model=Club
    
class MyClubUpDateView(UpdateView):
    
    #freeshool_myclubupdate.htmlをレンダリング（描写）する
    template_name='freeschool_myclubupdate.html'
    
    #モデルを指定する
    model=Club
    
    #フィールドを指定する
    fields=('club_name',
            'category',
            'REP',
            'email',
            'phone_number',
            'date',
            'fee',
            'place',
            'sns_link',
            'sns_name',
            'image1',
            'image2',
            'image3',
            'image4',
            'image5',
            'public_flag',
            'detail_text',
    )
    
    def get_success_url(self):
        #成功後の遷移先URL
        return reverse_lazy('freeschoolapp:myclubupdate', kwargs={'pk': self.object.pk})

class MyClubDeleteCheckView(DeleteView):
    
    #freeshool_myclubdeletecheck.htmlをレンダリング（描写）する
    template_name='freeschool_myclubdeletecheck.html'
    
    #モデルを指定する
    model=Club
    
    def get_success_url(self):
        #成功後の遷移先URL
        return reverse_lazy('freeschoolapp:myclubdeletedone')


class MyClubDeleteDoneView(TemplateView):
    
    #freeshool_myclubderetedoneview.htmlをレンダリング（描写）する
    template_name='freeschool_myclubdeletedone.html'

class EventPostView(BaseView,CreateView):

    #イベント掲載情報登録画面を表示
    template_name='freeschool_eventpost.html'
    #フォームとモデルを指定する
    form_class=EventPostForm
    form=EventPostForm
    model=Event
    
    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        #投稿フォームをcontextに格納
        context['eventpost_form']=self.form
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
        return reverse_lazy('freeschoolapp:eventpostdone')


class EventPostDoneView(TemplateView):
    
    #freshool_eventpostdone.htmlをレンダリング（描写）する
    template_name='freeschool_eventpostdone.html'


class MyEventListView(ListView):
    
    #freeschool_myeventlist.htmlをレンダリング（描写）する
    template_name='freeschool_myeventlist.html'
    
    #投稿されたイベントを投稿日時の降順（新しい順）に並べ替える
    queryset=Event.objects.order_by('-created_at')
    
    #1ページに表示する件数
    paginate_by=10


class MyEventDetailView(DetailView):
    
    #freeschool_myeventdetail.htmlをレンダリング（描写）する
    template_name='freeschool_myeventdetail.html'
    
    #モデルを指定する
    model=Event


class MyEventUpDateView(UpdateView):
    
    #freeshool_myeventupdate.htmlをレンダリング（描写）する
    template_name='freeschool_myeventupdate.html'
    
    #モデルを指定する
    model=Event
    
    #フィールドを指定する
    fields=('event_name',
            'category',
            'REP',
            'email',
            'phone_number',
            'date',
            'fee',
            'place',
            'sns_link',
            'sns_name',
            'image1',
            'image2',
            'image3',
            'image4',
            'image5',
            'public_flag',
            'detail_text',
    )
    
    def get_success_url(self):
        #成功後の遷移先URL
        return reverse_lazy('freeschoolapp:myeventupdate', kwargs={'pk': self.object.pk})


class MyEventDeleteCheckView(DeleteView):
    
    #freeshool_myeventdeletecheck.htmlをレンダリング（描写）する
    template_name='freeschool_myeventdeletecheck.html'
    
    #モデルを指定する
    model=Event
    
    def get_success_url(self):
        #成功後の遷移先URL
        return reverse_lazy('freeschoolapp:myeventdeletedone')


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

