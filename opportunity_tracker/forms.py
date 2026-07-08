from django import forms
from .models import Company, Opportunity, Contact, FollowUp, Notes



class CompanyForm(forms.ModelForm):
    
    class Meta:
        model = Company
        fields = "__all__"


class FollowUpForm(forms.ModelForm):

    class Meta:
        model = FollowUp
        fields = ['opportunity', 'contact', 'follow_up_date']
        widgets = {
            'follow_up_date': forms.widgets.DateInput(attrs={'type': 'date'})
        }

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            if getattr(self.instance, 'opportunity', None) is not None:
                self.fields['contact'].queryset = Contact.objects.filter(opportunities=self.instance.opportunity)
            else:
                self.fields['contact'].queryset = Contact.objects.none()
            

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
            'note': forms.widgets.Textarea(attrs={'rows': 12, 'cols': 120}),
            'date': forms.widgets.DateInput(attrs={'type': 'date'})
        }