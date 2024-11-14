from django.shortcuts import render
from django.views.generic.base import TemplateView

class LoginView(TemplateView):
    
    #freeschool_login.htmlをレンダリング（描写）する
    template_name='freeschool_login.html'


class TopView(TemplateView):
    
    #freeschool_top.htmlをレンダリング（描写）する
    template_name='freeschool_top.html'
    

class MailSendView(TemplateView):
    
    #freeschool_passwordreset.htmlをレンダリング（描写）する
    template_name='freeschool_mailsend.html'
    

class MailSendDoneView(TemplateView):
    
    #freeschool_mailsenddone.htmlをレンダリング（描写）する
    template_name='freeschool_mailsenddone.html'


class AccountView(TemplateView):
    
    #freeschool_account.htmlをレンダリング（描写）する
    template_name='freeschool_account.html'


class AccountUpdateView(TemplateView):
    
    #freeschool_accountupdate.htmlをレンダリング（描写）する
    template_name='freeschool_accountupdate.html'


class PasswordResetView(TemplateView):
    
    #freeschool_passwordreset.htmlをレンダリング（描写）する
    template_name='freeschool_passwordreset.html'


class PasswordResetDoneView(TemplateView):
    
    #freeschool_passwordresetdone.htmlをレンダリング（描写）する
    template_name='freeschool_passwordresetdone.html'


class UserSearchView(TemplateView):
    
    #freeschool_usersearch.htmlをレンダリング（描写）する
    template_name='freeschool_usersearch.html'


class UserDetailView(TemplateView):
    
    #freeschool_userdetail.htmlをレンダリング（描写）する
    template_name='freeschool_userdetail.html'