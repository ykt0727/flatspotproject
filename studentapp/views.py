from django.shortcuts import render,get_object_or_404,redirect
from django.views.generic import TemplateView,ListView,DetailView,FormView,UpdateView,DeleteView
from django.urls import reverse_lazy
from django.views import View
from django.contrib import messages
from django.contrib.auth import logout
from django.core.exceptions import PermissionDenied


#JSONファイルを扱うためのファイル
from django.http.response import JsonResponse

from django.core.mail import EmailMessage

#モデル、フォーム関連
from .models import CustomUser,Student,LikeForBlogPost,LikeForClub,LikeForEvent
from .forms import ClubRequestForm,EventRequestForm,ContactForm,CustomUserForm,StudentForm
from freeschoolapp.models import BlogPost,Club,Event,FreeSchool


class TopView(TemplateView):
    template_name = 'student_top.html'
    
    def dispatch(self, *args, **kwargs):
        # ログアウト状態か、ログイン状態でuser_typeが'student'か確認
        if not(not self.request.user.is_authenticated or (self.request.user.is_authenticated and self.request.user.user_type=='student')):
            # 条件を満たさない場合はアクセス拒否または別ページへリダイレクト
            return redirect('studentapp:logouturge')#ログアウトページにリダイレクト
        return super().dispatch(self.request,*args,**kwargs)
        
class ClubListView(ListView):
    #student_clublist.htmlをレンダリング（描写）する
    template_name=('student_clublist.html')
    #モデルを指定
    model=Club
    #モデルBlogPostのオブジェクトにquerysetを適用
    queryset=Club.objects.order_by('created_at')
    #1ページに表示するレコードの件数を設定
    paginate_by=5

    def get_queryset(self):
        queryset = Club.objects.order_by('-created_at')
        
        if self.request.user.is_authenticated and self.request.user.user_type=='student':
            #閲覧権限がない場合、publicの投稿のみ表示する
            if not self.request.user.student.is_view:
                queryset=queryset.filter(public_flag=True)  # ここでフィルタリングを適用

        category=self.request.GET.get('category')
        if category:
            queryset=queryset.filter(category=category)

        return queryset
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_choices'] = Club.category_choices  # 選択肢を追加
        context['selected_category'] = self.request.GET.get('category', '')  # 選択されたカテゴリを渡す
        return context
    
    def dispatch(self, *args, **kwargs):
        # ログアウト状態か、ログイン状態でuser_typeが'student'か確認
        if not(not self.request.user.is_authenticated or (self.request.user.is_authenticated and self.request.user.user_type=='student')):
            # 条件を満たさない場合はアクセス拒否または別ページへリダイレクト
            return redirect('studentapp:logouturge')#ログアウトページにリダイレクト
        return super().dispatch(self.request,*args,**kwargs)
    
class ClubDetailView(DetailView):
    template_name='student_clubdetail.html'
    #モデルを設定
    model=Club

    def get_context_data(self, **kwargs):
        # 親クラスのコンテキストデータを取得
        context = super().get_context_data(**kwargs)
        
        # 認証済みで学生の場合
        if self.request.user.is_authenticated and self.request.user.user_type == 'student':
            # 「いいね」済みかどうか判定
            context['user_has_liked'] = LikeForClub.objects.filter(
                target=self.object,
                user=self.request.user
            ).exists()

            # 閲覧権限のチェック
            if not self.request.user.student.is_view:
                # 権限がない場合、publicの投稿以外は表示しない
                if not self.object.public_flag:
                    raise PermissionDenied("このサークルを閲覧する権限がありません。")
        else:
            # 未認証ユーザーはpublicの投稿だけ許可
            if not self.object.public_flag:
                raise PermissionDenied("このサークルを閲覧する権限がありません。")

        return context
    
    def dispatch(self, *args, **kwargs):
        # ログアウト状態か、ログイン状態でuser_typeが'student'か確認
        if not(not self.request.user.is_authenticated or (self.request.user.is_authenticated and self.request.user.user_type=='student')):
            # 条件を満たさない場合はアクセス拒否または別ページへリダイレクト
            return redirect('studentapp:logouturge')#ログアウトページにリダイレクト
        return super().dispatch(self.request,*args,**kwargs)
    

#サークルのいいね機能のView
class LikeForClubView(View):
    def get(self,request,*args,**kwargs):
        #URLのパラメータからpkを取得
        club_id=self.kwargs.get('pk')      
        # 対象の投稿を取得
        club_post=get_object_or_404(Club,pk=club_id)

        # 現在のユーザーがすでに「いいね」をしているか確認、ユーザーがまだ「いいね」をしていない場合にCreateにTrueが返ってくる
        #まだユーザーがいいねをしていない場合は新たにいいねテーブルに追加
        like,created=LikeForClub.objects.get_or_create(
            target=club_post,
            user=request.user
        )

        #ユーザーがすでにいいねしている場合、いいねを取り消す
        if not created:
            # 既存の「いいね」があれば削除
            like.delete()
            return JsonResponse({'liked':False})
        
        # ユーザーがまだいいねしていない場合、新たに「いいね」を追加
        return JsonResponse({'liked':True})    

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
        subject='【ふらっとすぽっと】サークルに体験申請が来ました！'
        body=f'<h1>新しい体験申請がありました！</h1>'
        body+=f'<p>申請のあったサークル:{club.club_name}</p>'
        body+=f'<p><strong>申請者のメールアドレス:</strong> {sender_email}</p>'
        body+=f'<p>{self.request.user.student.nickname}さん</p>'
        if self.request.user.student.is_guardian:
            body+=f'<p>保護者の方からのメッセージです。</p>'
        if self.request.user.student.gender == 'male':
            body+=f'<p>性別:男性</p>'
        elif self.request.user.student.gender == 'female':
            body+=f'<p>性別:女性</p>'
        elif self.request.user.student.gender == 'unknown':
            body+=f'<p>性別:不明</p>'
        body+=f'<p>配慮事項:{self.request.user.student.consideration}</p>'
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
        messages.success(self.request, "送信が完了しました。")
        
        return super().form_valid(form)
    
    def dispatch(self, *args, **kwargs):
        # ログアウト状態か、ログイン状態でuser_typeが'student'か確認
        if not(not self.request.user.is_authenticated or (self.request.user.is_authenticated and self.request.user.user_type=='student')):
            # 条件を満たさない場合はアクセス拒否または別ページへリダイレクト
            return redirect('studentapp:logouturge')#ログアウトページにリダイレクト
        return super().dispatch(self.request,*args,**kwargs)
    
class ClubRequestDoneView(TemplateView):
    #student_clubrequestdone.htmlをレンダリング（描写）する 
    template_name="student_clubrequestdone.html"

    def dispatch(self, *args, **kwargs):
        # ログアウト状態か、ログイン状態でuser_typeが'student'か確認
        if not(not self.request.user.is_authenticated or (self.request.user.is_authenticated and self.request.user.user_type=='student')):
            # 条件を満たさない場合はアクセス拒否または別ページへリダイレクト
            return redirect('studentapp:logouturge')#ログアウトページにリダイレクト
        return super().dispatch(self.request,*args,**kwargs)
    
class EventListView(ListView):
    #student_eventlist.htmlをレンダリング（描写）する
    template_name=('student_eventlist.html')
    #モデルを指定
    model=Event
    #1ページに表示するレコードの件数を設定
    paginate_by=5

    def get_queryset(self):
        queryset = Event.objects.order_by('-created_at')
        
        if self.request.user.is_authenticated and self.request.user.user_type=='student':
            #閲覧権限がない場合、publicの投稿のみ表示する
            if not self.request.user.student.is_view:
                queryset=queryset.filter(public_flag=True)  # ここでフィルタリングを適用

        category=self.request.GET.get('category')
        if category:
            queryset=queryset.filter(category=category)

        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_choices'] = Event.category_choices  # 選択肢を追加
        context['selected_category'] = self.request.GET.get('category', '')  # 選択されたカテゴリを渡す
        return context
    
    def dispatch(self, *args, **kwargs):
        # ログアウト状態か、ログイン状態でuser_typeが'student'か確認
        if not(not self.request.user.is_authenticated or (self.request.user.is_authenticated and self.request.user.user_type=='student')):
            # 条件を満たさない場合はアクセス拒否または別ページへリダイレクト
            return redirect('studentapp:logouturge')#ログアウトページにリダイレクト
        return super().dispatch(self.request,*args,**kwargs)
    
class EventDetailView(DetailView):
    # student_eventdetail.htmlをレンダリング（描写）する
    template_name = 'student_eventdetail.html'
    model = Event

    def get_context_data(self, **kwargs):
        # 親クラスのコンテキストデータを取得
        context = super().get_context_data(**kwargs)
        
        # 認証済みで学生の場合
        if self.request.user.is_authenticated and self.request.user.user_type == 'student':
            # 「いいね」済みかどうか判定
            context['user_has_liked'] = LikeForEvent.objects.filter(
                target=self.object,
                user=self.request.user
            ).exists()

            # 閲覧権限のチェック
            if not self.request.user.student.is_view:
                # 権限がない場合、publicの投稿以外は表示しない
                if not self.object.public_flag:
                    raise PermissionDenied("このイベントを閲覧する権限がありません。")
        else:
            # 未認証ユーザーはpublicの投稿だけ許可
            if not self.object.public_flag:
                raise PermissionDenied("このイベントを閲覧する権限がありません。")

        return context
    
    def dispatch(self, *args, **kwargs):
        # ログアウト状態か、ログイン状態でuser_typeが'student'か確認
        if not(not self.request.user.is_authenticated or (self.request.user.is_authenticated and self.request.user.user_type=='student')):
            # 条件を満たさない場合はアクセス拒否または別ページへリダイレクト
            return redirect('studentapp:logouturge')#ログアウトページにリダイレクト
        return super().dispatch(self.request,*args,**kwargs)
    
#イベントのいいね機能のView
class LikeForEventView(View):
    def get(self,request,*args,**kwargs):
        #URLのパラメータからpkを取得
        event_id=self.kwargs.get('pk')      
        # 対象の投稿を取得
        club_post=get_object_or_404(Event,pk=event_id)

        # 現在のユーザーがすでに「いいね」をしているか確認、ユーザーがまだ「いいね」をしていない場合にCreateにTrueが返ってくる
        #まだユーザーがいいねをしていない場合は新たにいいねテーブルに追加
        like,created=LikeForEvent.objects.get_or_create(
            target=club_post,
            user=request.user
        )

        #ユーザーがすでにいいねしている場合、いいねを取り消す
        if not created:
            # 既存の「いいね」があれば削除
            like.delete()
            return JsonResponse({'liked':False})
        
        # ユーザーがまだいいねしていない場合、新たに「いいね」を追加
        return JsonResponse({'liked':True})    

class EventRequestView(FormView):
        
    #student_clubrequest.htmlをレンダリング（描写）する
    template_name="student_eventrequest.html"
    #クラス変数form_classに設定
    form_class=EventRequestForm
    #送信完了後遷移する
    success_url=reverse_lazy('studentapp:eventrequestdone')
    
    def get_initial(self):
        #初期値の取得
        initial=super().get_initial()
        
        #URLのパラメータからevent_idを取得
        event_id=self.kwargs.get('event_id') 
        
        #フォームに club_id を渡す
        initial['event_id']=event_id
        
        return initial
    
    #フォームのバリデーションを通過したデータがPOSTされたときに呼ばれるメール送信を行う
    def form_valid(self,form):
        
        #URLのパラメータからclub_idを取得
        event_id=self.kwargs.get('event_id')        
        #Clubオブジェクトを取得
        event=get_object_or_404(Event,pk=event_id)
        
        sender_email=self.request.user.email
        club_owner_email=event.email
        message=form.cleaned_data['message']
        
        # メールの内容をビューで動的に設定
        subject='【ふらっとすぽっと】イベント参加申請が来ました！'
        body=f'<h1>新しい申請がありました！</h1>'
        body+=f'<p>申請のあったイベント:{event.event_name}</p>'
        body+=f'<p><strong>申請者のメールアドレス:</strong> {sender_email}</p>'
        body+=f'<p>{self.request.user.student.nickname}さん</p>'
        if self.request.user.student.is_guardian:
            body+=f'<p>保護者の方からのメッセージです。</p>'
        if self.request.user.student.gender == 'male':
            body+=f'<p>性別:男性</p>'
        elif self.request.user.student.gender == 'female':
            body+=f'<p>性別:女性</p>'
        elif self.request.user.student.gender == 'unknown':
            body+=f'<p>性別:不明</p>'
        body+=f'<p>配慮事項:{self.request.user.student.consideration}</p>'
        
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
        messages.success(self.request, "送信が完了しました。")
        return super().form_valid(form)
    
    def dispatch(self, *args, **kwargs):
        # ログアウト状態か、ログイン状態でuser_typeが'student'か確認
        if not(not self.request.user.is_authenticated or (self.request.user.is_authenticated and self.request.user.user_type=='student')):
            # 条件を満たさない場合はアクセス拒否または別ページへリダイレクト
            return redirect('studentapp:logouturge')#ログアウトページにリダイレクト
        return super().dispatch(self.request,*args,**kwargs)
    
class EventRequestDoneView(TemplateView):
    #student_eventrequestdone.htmlをレンダリング（描写）する 
    template_name="student_eventrequestdone.html"
    
    def dispatch(self, *args, **kwargs):
        # ログアウト状態か、ログイン状態でuser_typeが'student'か確認
        if not(not self.request.user.is_authenticated or (self.request.user.is_authenticated and self.request.user.user_type=='student')):
            # 条件を満たさない場合はアクセス拒否または別ページへリダイレクト
            return redirect('studentapp:logouturge')#ログアウトページにリダイレクト
        return super().dispatch(self.request,*args,**kwargs)
    
#ブログ記事一覧
class BlogListView(ListView):
    #student_bloglist.htmlをレンダリング（描写）する
    template_name=('student_bloglist.html')
    #モデルを指定
    model=BlogPost
    #1ページに表示するレコードの件数を設定
    paginate_by=5
    def get_queryset(self):
        queryset = BlogPost.objects.order_by('-created_at')
        
        if self.request.user.is_authenticated and self.request.user.user_type=='student':
            #閲覧権限がない場合、publicの投稿のみ表示する
            if not self.request.user.student.is_view:
                queryset=queryset.filter(public_flag=True)  # ここでフィルタリングを適用

        category=self.request.GET.get('category')
        if category:
            queryset=queryset.filter(category=category)

        return queryset
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_choices'] = BlogPost.category_choices  # 選択肢を追加
        context['selected_category'] = self.request.GET.get('category', '')  # 選択されたカテゴリを渡す
        return context
    
        
    def dispatch(self, *args, **kwargs):
        # ログアウト状態か、ログイン状態でuser_typeが'student'か確認
        if not(not self.request.user.is_authenticated or (self.request.user.is_authenticated and self.request.user.user_type=='student')):
            # 条件を満たさない場合はアクセス拒否または別ページへリダイレクト
            return redirect('studentapp:logouturge')#ログアウトページにリダイレクト
        return super().dispatch(self.request,*args,**kwargs)
        
class BlogDetailView(DetailView):
    #student_blogdetail.htmlをレンダリング（描写）する
    template_name='student_blogdetail.html'
    #モデルを設定
    model=BlogPost
    
    def get_context_data(self, **kwargs):
        # 親クラスのコンテキストデータを取得
        context = super().get_context_data(**kwargs)
        
        # 認証済みで学生の場合
        if self.request.user.is_authenticated and self.request.user.user_type == 'student':
            # 「いいね」済みかどうか判定
            context['user_has_liked'] = LikeForBlogPost.objects.filter(
                target=self.object,
                user=self.request.user
            ).exists()

            # 閲覧権限のチェック
            if not self.request.user.student.is_view:
                # 権限がない場合、publicの投稿以外は表示しない
                if not self.object.public_flag:
                    raise PermissionDenied("このブログを閲覧する権限がありません。")
        else:
            # 未認証ユーザーはpublicの投稿だけ許可
            if not self.object.public_flag:
                raise PermissionDenied("このブログを閲覧する権限がありません。")

        return context
    
    def dispatch(self, *args, **kwargs):
        # ログアウト状態か、ログイン状態でuser_typeが'student'か確認
        if not(not self.request.user.is_authenticated or (self.request.user.is_authenticated and self.request.user.user_type=='student')):
            # 条件を満たさない場合はアクセス拒否または別ページへリダイレクト
            return redirect('studentapp:logouturge')#ログアウトページにリダイレクト
        return super().dispatch(self.request,*args,**kwargs)

#ブログのいいね機能のView
class LikeForBlogView(View):
    def get(self,request,*args,**kwargs):
        #URLのパラメータからpkを取得
        blog_id=self.kwargs.get('pk')      
        
        # 対象の投稿を取得
        blog_post=get_object_or_404(BlogPost,pk=blog_id)

        # 現在のユーザーがすでに「いいね」をしているか確認、ユーザーがまだ「いいね」をしていない場合にCreateにTrueが返ってくる
        #まだユーザーがいいねをしていない場合は新たにいいねテーブルに追加
        like,created=LikeForBlogPost.objects.get_or_create(
            target=blog_post,
            user=request.user
        )

        #ユーザーがすでにいいねしている場合、いいねを取り消す
        if not created:
            # 既存の「いいね」があれば削除
            like.delete()
            return JsonResponse({'liked':False})
        
        # ユーザーがまだいいねしていない場合、新たに「いいね」を追加
        return JsonResponse({'liked':True})    

#お問い合わせ
class ContactView(FormView):
    template_name ='student_contact.html'
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
        #送信先のメールアドレス
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
    
    def dispatch(self, *args, **kwargs):
        # ログアウト状態か、ログイン状態でuser_typeが'student'か確認
        if not(not self.request.user.is_authenticated or (self.request.user.is_authenticated and self.request.user.user_type=='student')):
            # 条件を満たさない場合はアクセス拒否または別ページへリダイレクト
            return redirect('studentapp:logouturge')#ログアウトページにリダイレクト
        return super().dispatch(self.request,*args,**kwargs)

#お問い合わせ完了画面
class ContactDoneView(TemplateView):
    #student_contactdone.htmlをレンダリング（描写）する
    template_name="student_contactdone.html"
    
    def dispatch(self, *args, **kwargs):
        # ログアウト状態か、ログイン状態でuser_typeが'student'か確認
        if not(not self.request.user.is_authenticated or (self.request.user.is_authenticated and self.request.user.user_type=='student')):
            # 条件を満たさない場合はアクセス拒否または別ページへリダイレクト
            return redirect('studentapp:logouturge')#ログアウトページにリダイレクト
        return super().dispatch(self.request,*args,**kwargs)
     
class AboutView(TemplateView):
    template_name="student_about.html"
    
    def dispatch(self, *args, **kwargs):
        # ログアウト状態か、ログイン状態でuser_typeが'student'か確認
        if not(not self.request.user.is_authenticated or (self.request.user.is_authenticated and self.request.user.user_type=='student')):
            # 条件を満たさない場合はアクセス拒否または別ページへリダイレクト
            return redirect('studentapp:logouturge')#ログアウトページにリダイレクト
        return super().dispatch(self.request,*args,**kwargs)

#アカウント情報表示画面
class MypageView(TemplateView):
    template_name='student_mypage.html'
    
    #コンテキスト情報にログイン中のユーザーの情報、ログインしたユーザーがいいねした情報を格納
    def get_context_data(self, **kwargs):
        #もともとあるコンテキスト情報を取得（ログイン情報）
        context=super().get_context_data(**kwargs)
        
        if self.request.user.is_authenticated and self.request.user.user_type=='student':
            #is_ViewがTrueの場合、全ての投稿を表示する
            if self.request.user.student.is_view:
                #ログインしているユーザーがいいねした記事を取得し、contextに格納する
                likeforblogposts=LikeForBlogPost.objects.filter(user=self.request.user).order_by('timestamp')
                context['likeforblogposts']=likeforblogposts
                likeforevents=LikeForEvent.objects.filter(user=self.request.user).order_by('timestamp')
                context['likeforevents']=likeforevents
                likeforclubs=LikeForClub.objects.filter(user=self.request.user).order_by('timestamp')
                context['likeforclubs']=likeforclubs
                return context
            else:
                #ログインしているユーザーがいいねした記事を取得し、contextに格納する
                likeforblogposts=LikeForBlogPost.objects.filter(user=self.request.user,target__public_flag=True).order_by('timestamp')
                context['likeforblogposts']=likeforblogposts
                likeforevents=LikeForEvent.objects.filter(user=self.request.user,target__public_flag=True).order_by('timestamp')
                context['likeforevents']=likeforevents
                likeforclubs=LikeForClub.objects.filter(user=self.request.user,target__public_flag=True).order_by('timestamp')
                context['likeforclubs']=likeforclubs
                return context
    
    def dispatch(self, *args, **kwargs):
        # ログアウト状態か、ログイン状態でuser_typeが'student'か確認
        if not(not self.request.user.is_authenticated or (self.request.user.is_authenticated and self.request.user.user_type=='student')):
            # 条件を満たさない場合はアクセス拒否または別ページへリダイレクト
            return redirect('studentapp:logouturge')#ログアウトページにリダイレクト
        return super().dispatch(self.request,*args,**kwargs)

#アカウント情報変更画面、UpdateViewでは原則一つのモデルしか扱えないため、Viewを使用する。
class MypageUpdateView(View):
    def get(self, request, *args, **kwargs):
        #フォームのインスタンスを作成
        user_form=CustomUserForm(instance=request.user)
        student_form=StudentForm(instance=request.user.student)
        
        # フォームをテンプレートに渡して表示
        return render(request, 'student_mypageupdate.html', {
            'user_form':user_form,
            'student_form':student_form,
        })
    
    def post(self, request, *args, **kwargs):
        #CustomuserとStudentを変更するフォームを定義する
        user_form=CustomUserForm(request.POST,instance=request.user)
        student_form=StudentForm(request.POST,instance=request.user.student)
        #バリデーションが通った場合のみデータベースに保存する
        if user_form.is_valid() and student_form.is_valid():
            user_form.save()
            student_form.save()
            messages.success(request, "アカウント情報が更新されました。")
            return redirect('studentapp:mypage')
        
        return render(request,'student_mypageupdate.html', {
            'user_form':user_form,
            'student_form':student_form,
        })
        
    def dispatch(self, *args, **kwargs):
        # ログアウト状態か、ログイン状態でuser_typeが'student'か確認
        if not(not self.request.user.is_authenticated or (self.request.user.is_authenticated and self.request.user.user_type=='student')):
            # 条件を満たさない場合はアクセス拒否または別ページへリダイレクト
            return redirect('studentapp:logouturge')#ログアウトページにリダイレクト
        return super().dispatch(self.request,*args,**kwargs)
    
#アカウント情報削除確認画面
class MypageDeleteCheckView(TemplateView):
    template_name="student_mypagedeletecheck.html"
    
    def dispatch(self, *args, **kwargs):
        # ログアウト状態か、ログイン状態でuser_typeが'student'か確認
        if not(not self.request.user.is_authenticated or (self.request.user.is_authenticated and self.request.user.user_type=='student')):
            # 条件を満たさない場合はアクセス拒否または別ページへリダイレクト
            return redirect('studentapp:logouturge')#ログアウトページにリダイレクト
        return super().dispatch(self.request,*args,**kwargs)

#アカウントを削除する処理
class AccountDeleteView(View):
    def post(self, request,*args,**kwargs):
        # 認証されたユーザーを削除
        user=request.user
        logout(request)  #セッションを終了
        user.delete()
        messages.success(request, "アカウントが正常に削除されました。")
        # ログアウト後のリダイレクト先を指定
        return redirect('studentapp:mypagedeletedone')
    
#アカウント削除完了画面
class MypageDeleteDoneView(TemplateView):
    template_name="student_mypagedeletedone.html"

class LogoutUrgeView(TemplateView):
    #freeschool_logouturge.htmlをレンダリング（描写）する
    template_name='student_logouturge.html'
    
#選択されたフリースクールの情報、関連した投稿を表示するページ
class FreeSchoolInfoView(DetailView):
    template_name='student_freeschoolinfo.html'
    model=FreeSchool
    
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        freeschool = self.get_object()
        #サークル、ブログ、イベントを取得
        context['clubs']=Club.objects.filter(user__freeschool=freeschool)
        context['events']=Event.objects.filter(user__freeschool=freeschool)
        context['blogposts']=BlogPost.objects.filter(user__freeschool=freeschool)
        return context