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