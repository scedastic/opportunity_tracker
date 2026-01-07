from django.contrib import admin
from .models import Opportunity, Contact, FollowUp, Notes, Stage

admin.site.site_title = "Opportunity Tracker site administration" 
admin.site.site_header = "Opportunity Tracker administration"
admin.site.index_title = "Opportunity Tracker administration"

class OpportunityAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'job_title', 'stack', 'open')
    search_fields = ('company_name', 'job_title', 'stack', 'assigned_to__username', 'stage__name')
    list_filter = ('stage', 'open')


class ContactAdmin(admin.ModelAdmin):
    list_display = ('name','opportunity')
    search_fields = ('opportunity__company_name',)


class NotesAdmin(admin.ModelAdmin):
    list_display = ('opportunity', 'date', 'note')
    search_fields = ('opportunity__company_name', 'note')
    list_filter = ('date','opportunity__company_name')


class FollowUpAdmin(admin.ModelAdmin):
    list_display = ('opportunity','follow_up_date','completed')
    list_filter = ('opportunity__open','completed')


admin.site.register(Opportunity, OpportunityAdmin)
admin.site.register(Contact, ContactAdmin)
admin.site.register(FollowUp, FollowUpAdmin)
admin.site.register(Notes, NotesAdmin)
admin.site.register(Stage)
