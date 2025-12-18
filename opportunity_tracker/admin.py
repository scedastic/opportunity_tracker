from django.contrib import admin
from .models import Opportunity, Contact, FollowUp, Notes, Stage

admin.site.site_title = "Opportunity Tracker site administration" 
admin.site.site_header = "Opportunity Tracker administration"
admin.site.index_title = "Opportunity Tracker administration"

admin.site.register(Opportunity)
admin.site.register(Contact)
admin.site.register(FollowUp)
admin.site.register(Notes)
admin.site.register(Stage)
