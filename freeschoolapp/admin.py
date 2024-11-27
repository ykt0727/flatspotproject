from django.contrib import admin

from .models import FreeSchool,Club,Event

#管理サイトでの表示をカスタムする
class FreeSchoolAdmin(admin.ModelAdmin):
    pass

#管理サイトにFreeSchoolとFreeSchooladminを追加する
admin.site.register(FreeSchool,FreeSchoolAdmin)

#管理サイトでの表示をカスタムする
class ClubAdmin(admin.ModelAdmin):
    pass

#管理サイトにClubを追加する
admin.site.register(Club,ClubAdmin)

#管理サイトでの表示をカスタムする
class EventAdmin(admin.ModelAdmin):
    pass

#管理サイトにEventを追加する
admin.site.register(Event,EventAdmin)