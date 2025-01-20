from django import forms
from .models import Club,Event,BlogPost,CustomUser,FreeSchool
from django.core.mail.message import EmailMessage

#サークル掲載フォーム
class ClubPostForm(forms.ModelForm):
    class Meta:
        model=Club
        #表示する項目
        fields=[
            'club_name',
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
        ]
        #画面に表示するラベルを設定する
        labels={
            'club_name':'サークル名',
            'category':'ジャンル',
            'REP':'代表者名',
            'email':'メールアドレス',
            'phone_number':'電話番号',
            'date':'日時',
            'fee':'参加費',
            'place':'場所',
            'sns_link':'SNSリンク',
            'sns_name':'SNS名',
            'image1':'画像1',
            'image2':'画像2',
            'image3':'画像3',
            'image4':'画像4',
            'image5':'画像5',
            'public_flag':'公開状況',
            'detail_text':'サークルの紹介文',
        }


#サークル掲載フォーム
class EventPostForm(forms.ModelForm):
    class Meta:
        model=Event
        #表示する項目
        fields=[
            'event_name',
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
        ]
        #画面に表示するラベルを設定する
        labels={
            'event_name':'イベント名',
            'category':'ジャンル',
            'REP':'代表者名',
            'email':'メールアドレス',
            'phone_number':'電話番号',
            'date':'日時',
            'fee':'参加費',
            'place':'場所',
            'sns_link':'SNSリンク',
            'sns_name':'SNS名',
            'image1':'画像1',
            'image2':'画像2',
            'image3':'画像3',
            'image4':'画像4',
            'image5':'画像5',
            'public_flag':'公開状況',
            'detail_text':'イベントの紹介文',
        }


class BlogPostForm(forms.ModelForm):
    
    title=forms.CharField(required=True)
    class Meta:
        model=BlogPost
        #表示するフィールド
        fields=[
                'title',
                'category',
                'image1',
                'image2',
                'image3',
                'image4',
                'image5',
                'public_flag',
                'detail_text',
                ]
        
        labels={
                'title':'タイトル',
                'category':'カテゴリー',
                'image1':'画像1',
                'image2':'画像2',
                'image3':'画像3',
                'image4':'画像4',
                'image5':'画像5',
                'public_flag':'公開状況',
                'detail_text':'記事内容',
        }
    
    # def clean(self):
    #     cleaned_data=super().clean()
    #     title=cleaned_data.get("title")
        
    #     if title and len(title)>10:
    #         self.add_error('title', 'タイトルを入力してください')
            
    #     return cleaned_data

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
        model=CustomUser
        #表示するフィールド
        fields = ['login_id','phone_number']

#FreeSchoolを変更するフォーム
class FreeSchoolForm(forms.ModelForm):
    class Meta:
            model=FreeSchool
            #表示するフィールド
            fields=['freeschool_name','address','manager_name']
