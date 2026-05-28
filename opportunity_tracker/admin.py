from django.contrib import admin
from .models import Company, Opportunity, Contact, FollowUp, Notes, Stage, StageHistory

admin.site.site_title = "Opportunity Tracker site administration" 
admin.site.site_header = "Opportunity Tracker administration"
admin.site.index_title = "Opportunity Tracker administration"

class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.action(description="Mark selected opportunities as abandoned")
def mark_as_abandoned(modeladmin, request, queryset):
    queryset.update(stage=Stage.objects.get(name="Abandoned"))

class OpportunityAdmin(admin.ModelAdmin):
    list_display = ('company__name', 'job_title', 'stack', 'initiation_date')
    search_fields = ('company__name', 'job_title', 'stack', 'stage__name')
    list_filter = ('stage', )
    actions=[mark_as_abandoned]


class ContactAdmin(admin.ModelAdmin):
    list_display = ('name','company','opportunity')
    search_fields = ('company__name',)


class NotesAdmin(admin.ModelAdmin):
    list_display = ('opportunity', 'date', 'note')
    search_fields = ('opportunity__company_name', 'note')
    list_filter = ('date','opportunity__company_name')


class FollowUpAdmin(admin.ModelAdmin):
    list_display = ('contact', 'follow_up_date','completed')
    list_filter = ('completed',)


class StageAdmin(admin.ModelAdmin):
    list_display = ('name','rank')


class StageHistoryAdmin(admin.ModelAdmin):
    list_display = ('transition_date', 'opportunity', 'new_stage')
    search_fields = ('opportunity__company_name',)
    list_filter = ('new_stage', )

admin.site.register(Company, CompanyAdmin)
admin.site.register(Opportunity, OpportunityAdmin)
admin.site.register(Contact, ContactAdmin)
admin.site.register(FollowUp, FollowUpAdmin)
admin.site.register(Notes, NotesAdmin)
admin.site.register(Stage, StageAdmin)
admin.site.register(StageHistory, StageHistoryAdmin)
