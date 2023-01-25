from django.contrib import admin
from .models import Opportunity, Contact, Notes, Stage

admin.site.register(Opportunity)
admin.site.register(Contact)
admin.site.register(Notes)
admin.site.register(Stage)
