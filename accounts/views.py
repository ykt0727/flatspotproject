from django.shortcuts import render
from django.views.generic.base import TemplateView,View
#リダイレクト
from django.shortcuts import redirect

#forms.pyで定義したフォーム
from .forms import SignupForm,StudentSignupForm,FreeSchoolSignupForm

#仮でTemplateViewを継承してlogin.htmlを描画する
class LoginView(TemplateView):
    template_name='login.html'
    
#student_signupdone.htmlをびょうふぁする
class SignupDoneView(TemplateView):
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
            
            # パラメータからリダイレクト先を取得,遷移前の画面でパラメータでnextを指定してください
            next_page=request.GET.get('next') or '/'
            return redirect(next_page)            
        
        #フォームが無効の場合再描画する
        return render(request,'student_signup.html',{
            'user_form':user_form,
            'student_form':student_form,
        })
            