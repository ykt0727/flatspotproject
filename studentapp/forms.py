from django import forms
from django.core.mail.message import EmailMessage

from .models import Student,CustomUser

import datetime

#サークル主催者に体験申請のメールを送るフォーム
class ClubRequestForm(forms.Form):
    
    message=forms.CharField(
        label='メッセージ',
        #複数行にわたって入力できるように設定
        widget=forms.Textarea(attrs={'class':'form-control','rows': 5}),
    )
    
    #不登校生徒とフリースクール関係者のメアドを引数で渡す
    def send_mail(self,sender_email,club_owner_email):
        
        subject="サークルに体験申請が来ました！"
        
        body="<h1><h1>"
        
        # メールの作成と送信
        email=EmailMessage(
            subject=subject,
            body=body,
            from_email=sender_email,
            to=[club_owner_email],
        )
        email.send()
        
#イベント主催者に参加申請のメールを送るフォーム
class EventRequestForm(forms.Form):
    
    message=forms.CharField(
        label='メッセージ',
        #複数行にわたって入力できるように設定
        widget=forms.Textarea(attrs={'class':'form-control','rows':5}),
    )
    
    #不登校生徒とフリースクール関係者のメアドを引数で渡す
    def send_mail(self,sender_email,club_owner_email):
        
        subject="イベントに体験申請が来ました！"
        
        body="<h1><h1>"
        
        # メールの作成と送信
        email=EmailMessage(
            subject=subject,
            body=body,
            from_email=sender_email,
            to=[club_owner_email],
        )
        email.send()

#お問い合わせフォーム
class ContactForm(forms.Form):
    name = forms.CharField(label='お名前')
    email = forms.EmailField(label='メールアドレス')
    title = forms.CharField(label='件名')
    message = forms.CharField(label='メッセージ',widget=forms.Textarea)

    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        
        self.fields['name'].widget.attrs['placeholder']='お名前を入力してください'
        self.fields['name'].widget.attrs['class']='form-control'
        
        self.fields['email'].widget.attrs['placeholder']='メールアドレスを入力してください'
        self.fields['email'].widget.attrs['class']='form-control'
        
        self.fields['title'].widget.attrs['placeholder']='タイトルを入力してください'
        self.fields['title'].widget.attrs['class']='form-control'
        
        self.fields['message'].widget.attrs['placeholder']='メッセージを入力してください'
        self.fields['message'].widget.attrs['class']='form-control'

#CustomUserを変更するフォーム
class CustomUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        #表示するフィールド
        fields = ['login_id','phone_number']
        labels={
           'login_id':'ログインID',
           'phone_number':'電話番号',
        }
    

#Studentを変更するフォーム
class StudentForm(forms.ModelForm):
    date_of_birth = forms.DateField(
        widget=forms.DateInput(
            attrs={'type': 'date'}  # HTML5のカレンダー入力を有効化
        ),
        label="誕生日"
    )
    class Meta:
        model=Student
        #表示するフィールド
        fields=['nickname','is_guardian','gender', 'ent_year', 'date_of_birth','consideration']
        labels={
           'nickname':'ニックネーム',
           'is_guardian':'保護者',
           'gender':'性別',
           'ent_year':'入学年度',
           'date_of_birth':'誕生日',
           'considerration':'配慮事項',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 現在の年月日を取得
        dt = datetime.datetime.now()
        now_month = dt.month
        now_year = dt.year if now_month >= 4 else dt.year - 1
        
        # 入学年度の選択肢生成（過去2年から今年まで）
        ent_year_choices = [(year, f"{year}年") for year in range(now_year - 2, now_year + 1)]
        self.fields['ent_year'].widget = forms.Select(choices=ent_year_choices)
        