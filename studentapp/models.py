from django.db import models
#カスタムユーザーのサブクラスとして実装
from accounts.models import CustomUser

class Student(models.Model):

    #CustomUserと1対1の関係にする、Studentが削除されたら親モデルも一緒に削除する
    user=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    
    #ニックネームを定義する
    nickname=models.CharField(max_length=25)
    
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
