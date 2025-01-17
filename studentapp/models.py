from django.db import models
#カスタムユーザーのサブクラスとして実装
from accounts.models import CustomUser
#サークル・イベント・ブログモデル
from freeschoolapp.models import Club,Event,BlogPost
#日付を取得する
from django.utils import timezone

class Student(models.Model):

    #CustomUserと1対1の関係にする、Studentが削除されたら親モデルも一緒に削除する
    user=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    
    #ニックネームを定義する
    nickname=models.CharField(unique=True,max_length=25)
    
    #保護者フラグ、デフォルトはFalse
    is_guardian=models.BooleanField(default=False)
   
    #閲覧権限フラグ、デフォルトはFalse
    is_view=models.BooleanField(default=False)
   
    # 性別フィールド（choicesを使用）
    GENDER_CHOICES=[
        ('male','男'),
        ('female','女'),
        ('unknown','不明'),
    ]

    gender=models.CharField(max_length=10,choices=GENDER_CHOICES,default='unknown')

    #入学年度
    ent_year=models.IntegerField()

    #生年月日フィールド
    date_of_birth=models.DateField()
   
    #配慮事項フィールド、テキスト形式で自由に入力できるようにする。
    consideration=models.TextField(blank=True,null=True)

#ブログのいいね機能
class LikeForBlogPost(models.Model):
    #いいねの対象、元の投稿が削除されたらいいねも削除する
    target=models.ForeignKey(BlogPost,on_delete=models.CASCADE)
    #いいねしたユーザー
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    #いいねした日付
    timestamp=models.DateTimeField(default=timezone.now)
    #データベースの初期設定をするクラス
    class Meta:
        #同じユーザーが同じ記事に対していいねできないようにする
        constraints = [
            models.UniqueConstraint(fields=['target','user'], name='unique_like_for_blogpost')
        ]
        
#サークルのいいね機能    
class LikeForClub(models.Model):
    #いいねの対象、元の投稿が削除されたらいいねも削除する
    target=models.ForeignKey(Club,on_delete=models.CASCADE)
    #いいねしたユーザー
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    #いいねした日付
    timestamp=models.DateTimeField(default=timezone.now)
    
    #データベースの初期設定をするクラス
    class Meta:
        #同じユーザーが同じ記事に対していいねできないようにする
        constraints = [
            models.UniqueConstraint(fields=['target','user'], name='unique_like_for_clubpost')
        ]
        

#イベントのイイネ機能
class LikeForEvent(models.Model):
    #いいねの対象、元の投稿が削除されたらいいねも削除する
    target=models.ForeignKey(Event,on_delete=models.CASCADE)
    #いいねしたユーザー
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    #いいねした日付
    timestamp=models.DateTimeField(default=timezone.now)
    
        #データベースの初期設定をするクラス
    class Meta:
        #同じユーザーが同じ記事に対していいねできないようにする
        constraints=[
            models.UniqueConstraint(fields=['target','user'], name='unique_like_for_eventpost')
        ]
        