from django.shortcuts import render,get_object_or_404,redirect
from django.views.generic import TemplateView,ListView,DetailView,FormView,UpdateView,DeleteView
from django.urls import reverse_lazy
from django.views import View
from django.contrib import messages
from django.contrib.auth import logout


#JSONファイルを扱うためのファイル
from django.http.response import JsonResponse

from django.core.mail import EmailMessage

#モデル、フォーム関連
from .models import CustomUser,Student,LikeForBlogPost,LikeForClub,LikeForEvent
from .forms import ClubRequestForm,EventRequestForm,ContactForm,CustomUserForm,StudentForm
from freeschoolapp.models import BlogPost,Club,Event


class TopView(View):
    template_name = 'student_top.html'

    def get_context_data(self, request):
        """共通処理: コンテキストを生成"""
        context = {}
        if request.user.is_authenticated and request.user.user_type == 'student':
            # 認証された学生に紐づく Student データを取得
            student=get_object_or_404(Student, user=request.user)
            context['student']=student
        else:
            context['error']="学生として認証されていません"
        return context

    def get(self, request, *args, **kwargs):
        """GETリクエストの処理"""
        context = self.get_context_data(request)
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        """POSTリクエストの処理"""
        context = self.get_context_data(request)
        return render(request, self.template_name, context)
        
class ClubListView(ListView):
    #student_clublist.htmlをレンダリング（描写）する
    template_name=('student_clublist.html')
    #モデルを指定
    model=Club
    #モデルBlogPostのオブジェクトにquerysetを適用
    queryset=Club.objects.order_by('created_at')
    #1ページに表示するレコードの件数を設定
    paginate_by=5
    
    def get_context_data(self, **kwargs):
        # 親のメソッドを呼び出して元々のコンテキストデータを取得
        context = super().get_context_data(**kwargs)
        
        # 認証されたユーザーが学生かどうかを確認
        if self.request.user.is_authenticated and self.request.user.user_type=='student':
            #認証された学生に紐づくStudentデータを取得
            student=get_object_or_404(Student, user=self.request.user)
            # コンテキストに追加
            context['student']=student
        
        return context
    
    
class ClubDetailView(DetailView):
    template_name='student_clubdetail.html'
    #モデルを設定
    model=Club

    def get_context_data(self, **kwargs):
        # 親のメソッドを呼び出して元々のコンテキストデータを取得
        context = super().get_context_data(**kwargs)
        
        # 認証されたユーザーが学生かどうかを確認
        if self.request.user.is_authenticated and self.request.user.user_type=='student':
            #認証された学生に紐づくStudentデータを取得
            student=get_object_or_404(Student, user=self.request.user)
            # コンテキストに追加
            context['student']=student
            
            #現在のユーザーがこの投稿に「いいね」しているかを確認、.exists()でTrueかFalseを返す
            context['user_has_liked']=LikeForClub.objects.filter(
                target=self.object,
                user=self.request.user
            ).exists()
        
        return context

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
    def get_context_data(self, **kwargs):
        # 親のメソッドを呼び出して元々のコンテキストデータを取得
        context = super().get_context_data(**kwargs)
        
        # 認証されたユーザーが学生かどうかを確認
        if self.request.user.is_authenticated and self.request.user.user_type=='student':
            #認証された学生に紐づくStudentデータを取得
            student=get_object_or_404(Student, user=self.request.user)
            # コンテキストに追加
            context['student']=student
        
        return context
    
class ClubRequestDoneView(TemplateView):
    #student_clubrequestdone.htmlをレンダリング（描写）する 
    template_name="student_clubrequestdone.html"

    def get_context_data(self, **kwargs):
        # 親のメソッドを呼び出して元々のコンテキストデータを取得
        context = super().get_context_data(**kwargs)
        
        # 認証されたユーザーが学生かどうかを確認
        if self.request.user.is_authenticated and self.request.user.user_type=='student':
            #認証された学生に紐づくStudentデータを取得
            student=get_object_or_404(Student, user=self.request.user)
            # コンテキストに追加
            context['student']=student
        
        return context
    
class EventListView(ListView):
    #student_eventlist.htmlをレンダリング（描写）する
    template_name=('student_eventlist.html')
    #モデルを指定
    model=Event
    #モデルBlogPostのオブジェクトにquerysetを適用
    queryset=Event.objects.order_by('created_at')
    #1ページに表示するレコードの件数を設定
    paginate_by=5
    def get_context_data(self, **kwargs):
        # 親のメソッドを呼び出して元々のコンテキストデータを取得
        context = super().get_context_data(**kwargs)
        
        # 認証されたユーザーが学生かどうかを確認
        if self.request.user.is_authenticated and self.request.user.user_type=='student':
            #認証された学生に紐づくStudentデータを取得
            student=get_object_or_404(Student, user=self.request.user)
            # コンテキストに追加
            context['student']=student
        return context
    
class EventDetailView(DetailView):
    #student_eventdetail.htmlをレンダリング（描写）する
    template_name='student_eventdetail.html'
    #モデルを設定
    model=Event
    def get_context_data(self, **kwargs):
        # 親のメソッドを呼び出して元々のコンテキストデータを取得
        context = super().get_context_data(**kwargs)
        
        # 認証されたユーザーが学生かどうかを確認
        if self.request.user.is_authenticated and self.request.user.user_type=='student':
            #認証された学生に紐づくStudentデータを取得
            student=get_object_or_404(Student, user=self.request.user)
            # コンテキストに追加
            context['student']=student
            
            #現在のユーザーがこの投稿に「いいね」しているかを確認、.exists()でTrueかFalseを返す
            context['user_has_liked']=LikeForEvent.objects.filter(
                target=self.object,
                user=self.request.user
            ).exists()
        
        
        return context
    
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

    def get_context_data(self, **kwargs):
        # 親のメソッドを呼び出して元々のコンテキストデータを取得
        context = super().get_context_data(**kwargs)
        
        # 認証されたユーザーが学生かどうかを確認
        if self.request.user.is_authenticated and self.request.user.user_type=='student':
            #認証された学生に紐づくStudentデータを取得
            student=get_object_or_404(Student, user=self.request.user)
            # コンテキストに追加
            context['student']=student
        
        return context
    
class EventRequestDoneView(TemplateView):
    #student_eventrequestdone.htmlをレンダリング（描写）する 
    template_name="student_eventrequestdone.html"

    def get_context_data(self, **kwargs):
        # 親のメソッドを呼び出して元々のコンテキストデータを取得
        context = super().get_context_data(**kwargs)
        
        # 認証されたユーザーが学生かどうかを確認
        if self.request.user.is_authenticated and self.request.user.user_type=='student':
            #認証された学生に紐づくStudentデータを取得
            student=get_object_or_404(Student, user=self.request.user)
            # コンテキストに追加
            context['student']=student
        
        return context
    
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
    def get_context_data(self, **kwargs):
        # 親のメソッドを呼び出して元々のコンテキストデータを取得
        context = super().get_context_data(**kwargs)
        
        # 認証されたユーザーが学生かどうかを確認
        if self.request.user.is_authenticated and self.request.user.user_type=='student':
            #認証された学生に紐づくStudentデータを取得
            student=get_object_or_404(Student, user=self.request.user)
            # コンテキストに追加
            context['student']=student
        
        return context
    
class BlogDetailView(DetailView):
    #student_blogdetail.htmlをレンダリング（描写）する
    template_name='student_blogdetail.html'
    #モデルを設定
    model=BlogPost
    
    def get_context_data(self, **kwargs):
        # 親のメソッドを呼び出して元々のコンテキストデータを取得
        context = super().get_context_data(**kwargs)
        
        # 認証されたユーザーが学生かどうかを確認
        if self.request.user.is_authenticated and self.request.user.user_type=='student':
            #認証された学生に紐づくStudentデータを取得
            student=get_object_or_404(Student, user=self.request.user)
            # コンテキストに追加
            context['student']=student
            
            # 現在のユーザーがこの投稿に「いいね」しているかを確認、.exists()でTrueかFalseを返す
            context['user_has_liked']=LikeForBlogPost.objects.filter(
                target=self.object,
                user=self.request.user
            ).exists()
            
        return context

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

#お問い合わせ完了画面
class ContactDoneView(TemplateView):
    #student_contactdone.htmlをレンダリング（描写）する
    template_name="student_contactdone.html"
    
    def get_context_data(self, **kwargs):
        # 親のメソッドを呼び出して元々のコンテキストデータを取得
        context=super().get_context_data(**kwargs)

        # 認証されたユーザーが学生かどうかを確認
        if self.request.user.is_authenticated and self.request.user.user_type=='student':
            #認証された学生に紐づくStudentデータを取得
            student=get_object_or_404(Student, user=self.request.user)
            # コンテキストに追加
            context['student']=student
        
        return context
     
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
    
    def get_context_data(self, **kwargs):
        
        # 親のメソッドを呼び出して元々のコンテキストデータを取得
        context = super().get_context_data(**kwargs)
        
        # 認証されたユーザーが学生かどうかを確認
        if self.request.user.is_authenticated and self.request.user.user_type=='student':
            #認証された学生に紐づくStudentデータを取得
            student=get_object_or_404(Student, user=self.request.user)
            # コンテキストに追加
            context['student']=student
        
        return context

#アカウント情報表示画面
class MypageView(TemplateView):
    template_name='student_mypage.html'
    
    #コンテキスト情報にログイン中のユーザーの情報、ログインしたユーザーがいいねした情報を格納
    def get_context_data(self, **kwargs):
        #もともとあるコンテキスト情報を取得（ログイン情報）
        context=super().get_context_data(**kwargs)
        
        if self.request.user.is_authenticated and self.request.user.user_type=='student':
            #認証ユーザーに紐づいているStudentの行を取得
            student=Student.objects.get(user=self.request.user)
            context['student']=student

            #ログインしているユーザーがいいねした記事を取得し、contextに格納する
            likeforblogposts=LikeForBlogPost.objects.filter(user=self.request.user).order_by('timestamp')
            context['likeforblogposts']=likeforblogposts
            likeforevents=LikeForEvent.objects.filter(user=self.request.user).order_by('timestamp')
            context['likeforevents']=likeforevents
            likeforclubs=LikeForClub.objects.filter(user=self.request.user).order_by('timestamp')
            context['likeforclubs']=likeforclubs
            
            return context

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
            return redirect('studentapp:mypage')
        return render(request,'student_mypageupdate.html', {
            'user_form':user_form,
            'student_form':student_form,
        })
        
#アカウント情報削除確認画面
class MypageDeleteCheckView(TemplateView):
    template_name="student_mypagedeletecheck.html"

#アカウントを削除する処理
class AccountDeleteView(View):
    def post(self, request,*args,**kwargs):
        # 認証されたユーザーを削除
        user=request.user
        logout(request)  #セッションを終了
        user.delete()
        # ログアウト後のリダイレクト先を指定
        return redirect('studentapp:mypagedeletedone')
    
#アカウント削除完了画面
class MypageDeleteDoneView(TemplateView):
    template_name="student_mypagedeletedone.html"
    