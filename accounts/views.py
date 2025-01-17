from django.shortcuts import render
from django.views.generic.base import TemplateView,View
from django.urls import reverse_lazy
#リダイレクト
from django.shortcuts import redirect
#Django標準のログインビュー
from django.contrib.auth.views import LoginView
#forms.pyで定義したフォーム
from .forms import SignupForm,StudentSignupForm,FreeSchoolSignupForm


#LoginViewを利用者別で変えられるように判別、'login.html'を描画する
class CustomLoginView(LoginView):
    template_name='login.html'
    def get_redirect_url(self):
        user=self.request.user
        #ユーザー認証が成功されている場合
        if user.is_authenticated:
            #利用者種別によって遷移されるページを変える
            if user.user_type=='student':
                return '../student/top'
            elif user.user_type=='freeschool':
                return '../freeschool/top'
        return super().get_redirect_url()

#student_signupdone.htmlを描画する
class StudentSignupDoneView(TemplateView):
    template_name='student_signupdone.html'

#不登校生徒用のサインアップビューを追加
class StudentSignupView(View):
    
    #サインアップフォームを表示する処理
    def get(self,request,*args,**kwargs):
        #CustomUserを作成するフォーム
        user_form=SignupForm()
        #Studentを作成するフォーム
        student_form=StudentSignupForm()

        #signup.htmlにフォームをレンダリングする
        return render(request,'student_signup.html',{
            'user_form':user_form,
            'student_form':student_form,
        })
        
    #サインアップする処理
    def post(self,request,*args,**kwargs):
        user_form= SignupForm(request.POST)
        student_form=StudentSignupForm(request.POST)
        
        # エラーが発生した場合のログ出力
        if not user_form.is_valid() or not student_form.is_valid():     
            print(user_form.errors)    
            print(student_form.errors)
        
        #バリデーションチェックを通った場合のみ処理する
        if user_form.is_valid() and student_form.is_valid():
            
            #CustomUserを作成する
            #コミットがTrueだと二重に保存されてしまうためFalseに設定する
            user=user_form.save(commit=False)
            #利用者種別を不登校生徒に固定
            user.user_type='student'
            #パスワードをハッシュ化
            user.set_password(user_form.cleaned_data['password'])
            user.save()
            
            #StudentUserを作成する
            #コミットがTrueだと二重に保存されてしまうためFalseに設定する
            student=student_form.save(commit=False)
            #CustomUserと関連付けする
            student.user=user
            student.save()
            
            #signupdoneにリダイレクトする
            return redirect('accounts:student_signupdone')            
        
        #フォームが無効の場合再描画する
        return render(request,'student_signup.html',{
            'user_form':user_form,
            'student_form':student_form,
        })