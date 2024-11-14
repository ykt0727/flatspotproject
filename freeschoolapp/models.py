from django.db import models
#継承専用のユーザークラス
from django.contrib.auth.models import AbstractBaseUser
#UUIDフィールド
import uuid
#電話番号フィールド
from phonenumber_field.modelfields import PhoneNumberField
# Create your models here.

class FreeSchoolUser(AbstractBaseUser):
    
    #UUIDを設定する
    id=models.UUIDField(primary_key=True, default=uuid.uuid4) 
    
    #フリースクール名
    freeschool_name=models.CharField(max_length=50,null=False)
    
    #責任者の名前
    manager_name=models.CharField(max_length=40,null=False)
    
    #ログイン用のユーザーIDを登録する
    login_id=models.CharField(unique=True,max_length=40,null=False)
    
    #電話番号フィールド、phonenumbersパッケージを使用する
    phone_number=PhoneNumberField(unique=True,null=False,)
    
    #住所フィールド
    address=models.CharField(max_length=255,null=False)
    
    #メールアドレス
    mail=models.EmailField(unique=True,null=False)
    
