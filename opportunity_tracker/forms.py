from django import forms
from .models import Opportunity, Contact, FollowUp, Notes


class FollowUpForm(forms.ModelForm):

    class Meta:
        model = FollowUp
        fields = ['opportunity', 'contact', 'follow_up_date']
        widgets = {
            'follow_up_date': forms.widgets.DateInput(attrs={'type': 'date'})
        }

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['contact'].queryset = Contact.objects.filter(opportunity=self.instance.opportunity)
            

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