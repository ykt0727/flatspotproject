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
    
    
class SessionTestView(TemplateView):
    
    #freeschool_sessiontest.htmlをレンダリング（描写）する
    template_name='freeschool_sessiontest.html'


class ClubPostView(TemplateView):
    
    #freeschool_clubpost.htmlをレンダリング（描写）する
    template_name='freeschool_clubpost.html'
    
    
class ClubPostCheckView(TemplateView):
    
    #freeschool_clubpostcheck.htmlをレンダリング（描写）する
    template_name='freeschool_clubpostcheck.html'
    

class ClubPostDoneView(TemplateView):
    
    #freeschool_clubpostdone.htmlをレンダリングする（描写）する
    template_name='freeschool_clubpostdone.html'

   
class MyClubListView(TemplateView):
    
    #freeschool_myclublist.htmlをレンダリング（描写）する
    template_name='freeschool_myclublist.html'
    

class EventPostView(TemplateView):
    
    #freeschool_eventpost.htmlをレンダリング（描写）する
    template_name='freeschool_eventpost.html'
    

class MyEventListView(TemplateView):
    
    #freeschool_myeventlist.htmlをレンダリング（描写）する
    template_name='freeschool_myeventlist.html'


class BlogPostView(TemplateView):
    
    #freeschool_blogpost.htmlをレンダリング（描写）する
    template_name='freeschool_blogpost.html'
    

class MyBlogListView(TemplateView):
    
    #freeschool_mybloglist.htmlをレンダリング（描写）する
    template_name='freeschool_mybloglist.html'
    
    
class MyBlogDetailView(TemplateView):
    #freeschool_myblogdetail.htmlをレンダリング（描写）する
    template_name='freeschool_myblogdetail.html'
    

