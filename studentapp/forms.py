from django import forms
from django.core.mail.message import EmailMessage

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
        
        self.fields['name'].widget.attrs['placeholder'] = 'お名前を入力してください'
        self.fields['name'].widget.attrs['class'] = 'form-control'
        
        self.fields['email'].widget.attrs['placeholder'] = 'メールアドレスを入力してください'
        self.fields['email'].widget.attrs['class'] = 'form-control'
        
        self.fields['title'].widget.attrs['placeholder'] = 'タイトルを入力してください'
        self.fields['title'].widget.attrs['class'] = 'form-control'
        
        self.fields['message'].widget.attrs['placeholder'] = 'メッセージを入力してください'
        self.fields['message'].widget.attrs['class'] = 'form-control'