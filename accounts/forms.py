from django import forms
from accounts.models import CustomUser
from studentapp.models import Student
from freeschoolapp.models import FreeSchool

#時刻関連
import datetime

#共通のサインアップフォーム
class SignupForm(forms.ModelForm):

    # パスワードを再確認するフィールドを追加
    password=forms.CharField(widget=forms.PasswordInput,label='パスワード')
    confirm_password=forms.CharField(widget=forms.PasswordInput,label='パスワード(確認)')
    
    #メタクラス
    class Meta:
        model=CustomUser
        #フォームを表示する項目、利用者種別は表示しない
        fields=['login_id','mail','phone_number','password']
        #画面に表示するラベルを設定する
        labels={
            'login_id':'ID',
            'mail':'メールアドレス',
            'phone_number':'電話番号',
        }

    #バリデーションを実行
    def clean(self):
        cleaned_data=super().clean()
        #パスワード(1回目)
        password=cleaned_data.get("password")
        #パスワード(再確認)
        confirm_password=cleaned_data.get("confirm_password")

        if password!=confirm_password:
            raise forms.ValidationError("パスワードが一致しません。")
        return cleaned_data

#不登校生徒用のサインアップフォーム
class StudentSignupForm(forms.ModelForm):
    class Meta:
        model=Student
        #表示するフィールド
        fields=['nickname','gender','ent_year','is_guardian','date_of_birth','consideration']
        #画面に表示するラベルを設定する
        labels={
            'nickname':'ニックネーム',
            'gender':'性別',
            'ent_year':'入学年度',
            'is_guardian':'保護者の方はチェックしてください',
            'date_of_birth':'誕生日',
            'consideration':'配慮事項'
        }
    # 日付を選択できるフォームフィールド
    date_of_birth=forms.DateField(widget=forms.DateInput(attrs={'type':'date'}))    
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
   
        #現在の年月日を取得し、保存する
        dt=datetime.datetime.now()
        #現在の月を取得する
        now_month=dt.month
        #4月~12月と1月~3月で処理を分岐させる
        if now_month >= 4:
        #現在の年を取得する
            now_year=dt.year
        else:
        #現在の年－1を取得する
            now_year=dt.year-1                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            
        #選択肢を生成
        ent_year_choices=[(year,f"{year}年") for year in range(now_year-2,now_year+1)]
        
        self.fields['ent_year'].widget=forms.Select(choices=ent_year_choices)
        
            
#フリースクール関係者用のサインアップフォーム(現時点だと使う必要なし)
class FreeSchoolSignupForm(forms.ModelForm):
    class Meta:
        model=FreeSchool
        #表示するフィールド
        fields=['freeschool_name','manager_name','address']
    
    