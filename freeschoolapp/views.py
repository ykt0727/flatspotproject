from django.shortcuts import render,redirect
from django.views.generic.base import TemplateView
from django.views import View
from .models import CustomUser,FreeSchool,Club,Event,BlogPost
from .forms import ClubPostForm,EventPostForm,BlogPostForm,ContactForm,CustomUserForm,FreeSchoolForm
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView,ListView,DetailView,UpdateView,DeleteView,FormView
from django.urls import reverse_lazy
from studentapp.models import Student
from django.core.mail import EmailMessage
from django.contrib import messages

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

class TopView(TemplateView):
    #freeschool_top.htmlをレンダリング（描写）する
    template_name='freeschool_top.html'

#ユーザー検索画面
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


class BlogPostView(CreateView):
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


class MyBlogListView(ListView):
    
    #freeschool_mybloglist.htmlをレンダリング（描写）する
    template_name='freeschool_mybloglist.html'
    
    #投稿されたイベントを投稿日時の降順（新しい順）に並べ替える
    queryset=BlogPost.objects.order_by('-created_at')
    
    #1ページに表示する件数
    paginate_by=10   
    
class MyBlogDetailView(DetailView):
    
    #freeschool_myblogdetail.htmlをレンダリング（描写）する
    template_name='freeschool_myblogdetail.html'
    
    model=BlogPost
    

class MyBlogUpDateView(UpdateView):
    
    #freeschool_myblogupdate.htmlをレンダリング（描写）する
    template_name='freeschool_myblogupdate.html'
    #モデルを指定する
    model=BlogPost
    
    #フィールドを指定する
    fields=('title',
            'category',
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


class MyBlogDeleteCheckView(DeleteView):
    
    #freeschool_myblogdeletecheck.htmlをレンダリング（描写）する
    template_name='freeschool_myblogdeletecheck.html'
    
    #モデルを指定する
    model=BlogPost
    
    def get_success_url(self):
        #成功後の遷移先URL
        return reverse_lazy('freeschoolapp:myeventdeletedone')


    
class MyBlogDeleteDoneView(TemplateView):
    
    #freeschool_myblogdeeltedone.htmlをレンダリング（描写）する
    template_name='freeschool_myblogdeletedone.html'


class ContactView(FormView):
    
    template_name ='freeschool_contact.html'
    form_class=ContactForm
    success_url=reverse_lazy('studentapp:contactdone')
    
    def form_valid(self, form):
        name=form.cleaned_data['name']
        email=form.cleaned_data['email']
        title=form.cleaned_data['title']
        message=form.cleaned_data['message']
        
        subject=f'お問い合わせ: {title}'
        
        message=\
            f'送信者名: {name}\nメールアドレス:{email}\n タイトル{title}\n メッセージ:{message}'
        
        #送信元メールアドレス
        from_email=email
        #送信先のメールアドレス(システム管理者のメールアドレス)
        to_list=['ymg2365013@stu.o-hara.ac.jp']
        
        message=EmailMessage(
                            subject=subject,
                            body=message,
                            from_email=from_email,
                            to=to_list,
                        )
        message.send()
        messages.success(
            self.request,'お問い合わせは正常に送信されました。')
            
        return super().form_valid(form)

#お問い合わせ完了画面
class ContactDoneView(TemplateView):
    #freeschool_contactdone.htmlをレンダリング（描写）する
    template_name='freeschool_contactdone.html'
    
#アカウント情報表示画面
class MypageView(TemplateView):
    template_name='freeschool_mypage.html'
    
    #コンテキスト情報にログイン中のユーザーの情報、ログインしたユーザーがいいねした情報を格納
    def get_context_data(self, **kwargs):
        #もともとあるコンテキスト情報を取得（ログイン情報）
        context=super().get_context_data(**kwargs)
        
        if self.request.user.is_authenticated and self.request.user.user_type=='freeschool':
            #認証ユーザーに紐づいているStudentの行を取得
            freeschool=FreeSchool.objects.get(user=self.request.user)
            context['freeschool']=freeschool
            return context

#アカウント情報変更画面、UpdateViewでは原則一つのモデルしか扱えないため、Viewを使用する。
class MypageUpdateView(View):
    def get(self, request, *args, **kwargs):
        #フォームのインスタンスを作成
        user_form=CustomUserForm(instance=request.user)
        freeschool_form=FreeSchoolForm(instance=request.user.freeschool)
        
        # フォームをテンプレートに渡して表示
        return render(request, 'freeschool_mypageupdate.html',{
            'user_form':user_form,
            'freeschool_form':freeschool_form,
        })
    
    def post(self, request, *args, **kwargs):
        #CustomuserとStudentを変更するフォームを定義する
        user_form=CustomUserForm(request.POST,instance=request.user)
        freeschool_form=FreeSchoolForm(request.POST,instance=request.user.freeschool)
        #バリデーションが通った場合のみデータベースに保存する
        if user_form.is_valid() and freeschool_form.is_valid():
            user_form.save()
            freeschool_form.save()
            return redirect('freeschoolapp:mypage')
        return render(request,'freeschool_mypageupdate.html',{
            'user_form':user_form,
            'freeschool_form':freeschool_form,
        })

#削除予定
class AccountView(TemplateView):
    template_name="freeschool_account.html"
    

        

