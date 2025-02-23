from django.db import models

#カスタムユーザーのサブクラスとして実装
from accounts.models import CustomUser
#電話番号のバリデーター
from django.core.validators import RegexValidator

class FreeSchool(models.Model):

    #CustomUserと1対多の関係にする、FreeSchoolが削除されたら親モデルも一緒に削除する
    user=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    
    #フリースクール名
    freeschool_name=models.CharField(max_length=50,null=False)
   
    #責任者の名前
    manager_name=models.CharField(max_length=40,null=False)
    
    #住所フィールド
    address=models.CharField(max_length=255,null=False)   
    
    def __str__(self):
        return self.freeschool_name  # 管理画面に表示する名前を freeschool_name に変更

class Club(models.Model):
    
    #CustomUserと1対多の関係にする、Clubが削除されたら親モデルも一緒に削除する
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    
    #サークル名
    club_name=models.CharField(max_length=50,null=False)
    
    #ジャンル
    category_choices=[
        ('culture','文化'),
        ('sports','運動'),
        ('study','勉強'),
        ('others','その他'),
    ]
    
    category=models.CharField(max_length=20,choices=category_choices)
    
    #代表者名
    REP=models.CharField(max_length=30,null=False)
    
    #メールアドレス
    email=models.EmailField(null=False)
    
    #電話番号
    phone_number = models.CharField(
        max_length=11,
        validators=[
            RegexValidator(regex=r"^\d+$", message="電話番号は半角数字11桁以内で入力してください。")
        ],
        unique=False,
        blank=False,
        null=False,
    )
    
    #日時
    date=models.CharField(max_length=30,null=False)
    
    #参加費
    fee=models.PositiveIntegerField(null=False)
    
    #場所
    place=models.CharField(max_length=50,null=False)
    
    #SNSリンク
    sns_link=models.URLField(null=False)
    
    #SNS名
    sns_name=models.CharField(max_length=30,null=False)
    
    #画像1~5
    image1=models.ImageField(blank=False,null=False,upload_to='photos')
    image2=models.ImageField(blank=True,null=True,upload_to='photos')
    image3=models.ImageField(blank=True,null=True,upload_to='photos')
    image4=models.ImageField(blank=True,null=True,upload_to='photos')
    image5=models.ImageField(blank=True,null=True,upload_to='photos')
    
    #公開状況
    public_flag=models.BooleanField(default=True)
    
    #サークルの紹介文
    detail_text=models.TextField(max_length=1000,blank=True,null=True)
    
    #作成日時
    created_at=models.DateTimeField(auto_now_add=True)
 
    #更新日時
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.club_name  # 管理画面に表示する名前をclub_nameに変更


class Event(models.Model):
    
    #CustomUserと1対多の関係にする、Eventが削除されたら親モデルも一緒に削除する
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    
    #イベント名
    event_name=models.CharField(max_length=50,null=False)
    
    #ジャンル
    category_choices=[
        ('culture','文化'),
        ('sports','運動'),
        ('study','勉強'),
        ('others','その他'),
    ]
    
    category=models.CharField(max_length=20,choices=category_choices)
    
    #代表者名
    REP=models.CharField(max_length=30,null=False)
    
    #メールアドレス
    email=models.EmailField(null=False)
    
    #電話番号
    phone_number = models.CharField(
        max_length=11,
        validators=[
            RegexValidator(regex=r"^\d+$", message="電話番号は半角数字11桁以内で入力してください。")
        ],
        unique=False,
        blank=False,
        null=False,
    )
    
    #日時
    date=models.CharField(max_length=30,null=False)
    
    #参加費
    fee=models.PositiveIntegerField(null=False)
    
    #場所
    place=models.CharField(max_length=50,null=False)
    
    #SNSリンク
    sns_link=models.URLField(null=False)
    
    #SNS名
    sns_name=models.CharField(max_length=30,null=False)
    
    #画像1~5
    image1=models.ImageField(blank=False,null=False,upload_to='photos')
    image2=models.ImageField(blank=True,null=True,upload_to='photos')
    image3=models.ImageField(blank=True,null=True,upload_to='photos')
    image4=models.ImageField(blank=True,null=True,upload_to='photos')
    image5=models.ImageField(blank=True,null=True,upload_to='photos')
    
    #公開状況
    public_flag=models.BooleanField(default=True)
    
    #イベントの紹介文
    detail_text=models.TextField(max_length=1000,blank=True,null=True)
    
    #作成日時
    created_at=models.DateTimeField(auto_now_add=True)
 
    #更新日時
    updated_at=models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.event_name  # 管理画面に表示する名前をevent_nameに変更

class BlogPost(models.Model):
   
    #投稿者を紐づける
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    
    #タイトル
    title=models.CharField(max_length=40,null=False)
    
    #ジャンル
    category_choices=[
        ('report','活動報告'),
        ('news','ニュース'),
    ]
    category=models.CharField(max_length=25,choices=category_choices)
    
    #画像1~5、1枚目は必須
    image1=models.ImageField(blank=False,null=False,upload_to='photos')
    image2=models.ImageField(blank=True,null=True,upload_to='photos')
    image3=models.ImageField(blank=True,null=True,upload_to='photos')
    image4=models.ImageField(blank=True,null=True,upload_to='photos')
    image5=models.ImageField(blank=True,null=True,upload_to='photos')
   
    #公開状況
    public_flag=models.BooleanField(default=True)
   
    #ブログ記事本文
    detail_text=models.TextField(max_length=1000,blank=True,null=True)
 
    #作成日時
    created_at=models.DateTimeField(auto_now_add=True)
 
    #更新日時
    updated_at=models.DateTimeField(auto_now=True)

    #管理画面に表示する名前をtitleに変更
    def __str__(self):
        return self.title 