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
    

class MyClubDetailView(TemplateView):
    
    #freeschool_myclubdetail.htmlをレンダリング（描写）する
    template_name='freeschool_myclubdetail.html'
    
class MyClubUpDateView(TemplateView):
    
    #freeshool_myclubupdate.htmlをレンダリング（描写）する
    template_name='freeschool_myclubupdate.html'

class MyClubDeleteCheckView(TemplateView):
    
    #freeshool_myclubdeletecheck.htmlをレンダリング（描写）する
    template_name='freeschool_myclubdeletecheck.html'


class MyClubDeleteDoneView(TemplateView):
    
    #freeshool_myclubderetedoneview.htmlをレンダリング（描写）する
    template_name='freeschool_myclubdeletedone.html'

class EventPostView(TemplateView):
    
    #freeschool_eventpost.htmlをレンダリング（描写）する
    template_name='freeschool_eventpost.html'
    

class EventPostCheckView(TemplateView):
    
    #freshool_eventpostcheck.htmlをレンダリング（描写）する
    template_name='freeschool_eventpostcheck.html'


class EventPostDoneView(TemplateView):
    
    #freshool_eventpostdone.htmlをレンダリング（描写）する
    template_name='freeschool_eventpostdone.html'


class MyEventListView(TemplateView):
    
    #freeschool_myeventlist.htmlをレンダリング（描写）する
    template_name='freeschool_myeventlist.html'


class MyEventDetailView(TemplateView):
    
    #freeschool_myeventdetail.htmlをレンダリング（描写）する
    template_name='freeschool_myeventdetail.html'


class MyEventUpDateView(TemplateView):
    
    #freeschool_myeventupdate.htmlをレンダリング（描写）する
    template_name='freeschool_myeventupdate.html'


class MyEventDeleteCheckView(TemplateView):
    
    #freeschool_myeventdeleteCheck.htmlをレンダリング（描写）する
    template_name='freeschool_myeventdeletecheck.html'


class MyEventDeleteDoneView(TemplateView):
    
    #freeschool_myeventdeletedone.htmlをレンダリング（描写）する
    template_name='freeschool_myeventdeletedone.html'


class BlogPostView(TemplateView):
    
    #freeschool_blogpost.htmlをレンダリング（描写）する
    template_name='freeschool_blogpost.html'
    

class BlogPostCheckView(TemplateView):
    
    #freeschool_blogpostcheck.htmlをレンダリング（描写）する
    template_name='freeschool_blogpostcheck.html'


class MyBlogListView(TemplateView):
    
    #freeschool_mybloglist.htmlをレンダリング（描写）する
    template_name='freeschool_mybloglist.html'
    
    
class MyBlogDetailView(TemplateView):
    
    #freeschool_myblogdetail.htmlをレンダリング（描写）する
    template_name='freeschool_myblogdetail.html'
    

class MyBlogUpDateView(TemplateView):
    
    #freeschool_myblogupdate.htmlをレンダリング（描写）する
    template_name='freeschool_myblogupdate.html'


class MyBlogDeleteCheckView(TemplateView):
    
    #freeschool_myblogdeletecheck.htmlをレンダリング（描写）する
    template_name='freeschool_myblogdeletecheck.html'
    
    
class MyBlogDeleteDoneView(TemplateView):
    
    #freeschool_myblogdeeltedone.htmlをレンダリング（描写）する
    template_name='freeschool_myblogdeletedone.html'


class ContactView(TemplateView):
    
    #freeschool_contact.htmlをレンダリング(描写)する
    template_name='freeschool_contact.html'


class ContactDoneView(TemplateView):
    
    #freeschool_contactdone.htmlをレンダリング（描写）する
    template_name='freeschool_contactdone.html'

