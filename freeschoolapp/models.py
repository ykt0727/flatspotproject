from django.db import models

#カスタムユーザーのサブクラスとして実装
from accounts.models import CustomUser

class FreeSchool(models.Model):

    #CustomUserと1対1の関係にする、FreeSchoolが削除されたら親モデルも一緒に削除する
    user=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    
    #フリースクール名
    freeschool_name=models.CharField(max_length=50,null=False)
   
    #責任者の名前
    manager_name=models.CharField(max_length=40,null=False)
    
    #住所フィールド
    address=models.CharField(max_length=255,null=False)    