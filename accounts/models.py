from django.db import models

#継承専用のユーザ作成用抽象クラス
from django.contrib.auth.models import AbstractBaseUser
#UUIDフィールド
import uuid
#電話番号フィールド
from phonenumber_field.modelfields import PhoneNumberField
#日付を取得する
from django.utils import timezone

#認証モデル、パスワードは暗黙的に定義されている
class BaseUser(AbstractBaseUser):
    #UUIDを設定する
    uu_id=models.UUIDField(primary_key=True,default=uuid.uuid4)
    #ログインに使用するユーザーIDを設定する
    login_id=models.CharField(max_length=40,unique=True,null=False)
    #登録日
    date_joined=models.DateTimeField("登録日",default=timezone.now)
    
    #メールフィールド
    mail=models.EmailField(unique=True)
    
    #電話番号フィールド、phonenumbersパッケージを使用する
    phone_number=PhoneNumberField(unique=True,null=True,blank=True)
    
    #利用者種別の選択肢
    user_type_choices=(
        ('student','不登校生徒'),
        ('freeschool','フリースクール関係者'),
    )
    
    #利用者種別
    user_type=models.CharField(max_length=20,choices=user_type_choices)
    
    #ログインIDで認証
    USERNAME_FIELD='login_id'
    
    #ユーザー作成時にメールと利用者種別を必須にする
    REQUIRED_FIELDS=['mail','user_type'] 
    
    #カスタムユーザーマネージャーを設定
    #objects = CustomUserManager()
    