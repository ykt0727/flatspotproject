from django import forms
from .models import Club,BlogPost

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


class BlogPostForm(forms.ModelForm):
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