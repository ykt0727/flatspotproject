from django.db import models

#継承専用のユーザ作成用抽象クラス、マネージャーのベース
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin,BaseUserManager
#UUIDフィールド
import uuid
#電話番号フィールド
from phonenumber_field.modelfields import PhoneNumberField
#日付を取得する
from django.utils import timezone

#カスタムユーザーのマネージャー
class CustomUserManager(BaseUserManager):

    #不登校生徒とフリースクール関係者のユーザーを作成するメソッド

    def create_user(self,login_id,password,**extra_fields):
        
        #ログインIDが設定されているか判別
        if not login_id:
            raise ValueError('ログインIDが設定されていません')
        
        #メールの正規化を行う
        extra_fields['mail']=self.normalize_email(extra_fields.get('mail'))
        
        #インスタンスを作成
        user=self.model(login_id=login_id,**extra_fields)
        #パスワードを設定する
        user.set_password(password)
        #データベースに格納する
        user.save(using=self._db)
        return user        
            
    #スーパーユーザーを作成する際のメソッド、設定時にlogin_idとpasswordを設定する
    def create_superuser(self,login_id,password,**extra_fields):
        
        #デフォルトでスタッフ権限と管理者権限をTrueとする
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        #スタッフ権限とスーパーユーザー権限がTrueかチェックする
        if extra_fields.get('is_staff') is not True:
            raise ValueError('is_staffはTrueにしてください')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('is_superuserはTrueにしてください')
        
        #メールの正規化を行う
        extra_fields['mail']=self.normalize_email(extra_fields.get('mail'))
        
        return self.create_user(login_id,password,**extra_fields)

#認証モデル、パスワードは暗黙的に定義されている
class CustomUser(AbstractBaseUser,PermissionsMixin):
    #UUIDを設定する
    uu_id=models.UUIDField(primary_key=True,default=uuid.uuid4)
    
    #ログインに使用するユーザーIDを設定する
    login_id=models.CharField(max_length=40,unique=True,null=False)
    
    #登録日
    date_joined=models.DateTimeField("登録日",default=timezone.now)
    
    #メールフィールド
    mail=models.EmailField(unique=True)
    
    #電話番号フィールド、phonenumbersパッケージを使用する
    phone_number=PhoneNumberField(unique=True,null=True,blank=True,region='JP')
    
    #利用者種別の選択肢
    user_type_choices=(
        ('student','不登校生徒'),
        ('freeschool','フリースクール関係者'),
    )
    
    #利用者種別
    user_type=models.CharField(max_length=20,choices=user_type_choices)
    
    #is_staffとis_superuserを追加
    is_staff=models.BooleanField(default=False)
    is_superuser=models.BooleanField(default=False)
    
    #ログインIDで認証
    USERNAME_FIELD='login_id'
    
    #ユーザー作成時に必須にする項目
    REQUIRED_FIELDS=['mail'] 
    
    #データベースを操作するためのマネージャーを登録
    objects=CustomUserManager()