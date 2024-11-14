from django.db import models
#継承専用のユーザークラス
from django.contrib.auth.models import AbstractUser
#UUIDフィールド
import uuid
#電話番号フィールド
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.

class FreeSchoolUser(AbstractUser):
    #UUIDを設定する
    id=models.UUIDField(primary_key=True, default=uuid.uuid4) 
    
    #ニックネームを定義する
    nickname=models.CharField(max_length=25)
    
    #保護者フラグ、デフォルトはFalse
    is_guardian=models.BooleanField(default=False)
    
    #閲覧権限フラグ、デフォルトはFalse
    is_view=models.BooleanField(default=False)
    
    # 性別フィールド（choicesを使用）
    GENDER_CHOICES=[
        ('male', '男'),
        ('female', '女'),
        ('unknown', '不明'),
    ]
    gender=models.CharField(max_length=10, choices=GENDER_CHOICES, default='unknown')

    #入学年度
    ent_year=models.IntegerField()
    
    #電話番号フィールド、phonenumbersパッケージを使用する
    phone_number=PhoneNumberField(unique=True, null=True, blank=True)
    
    #生年月日フィールド
    date_of_birth=models.DateField()
    
    #配慮事項フィールド、テキスト形式で自由に入力できるようにする。
    consideration=models.TextField(blank=True, null=True)