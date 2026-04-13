from django import forms
from .models import Opportunity, Contact, FollowUp, Notes

class OpportunityForm(forms.ModelForm): 

    class Meta:
        model = Opportunity
        fields = "__all__"
        widgets = {
            'initiation_date': forms.widgets.DateInput(attrs={'type': 'date'})
        }

class NoteForm(forms.ModelForm):

    class Meta:
        model = Notes
        fields = "__all__"
        widgets = {
            'date': forms.widgets.DateInput(attrs={'type': 'date'})
        }