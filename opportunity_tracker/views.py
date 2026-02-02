import datetime
from urllib import response
from django.db.models import Q, Count
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from .models import Opportunity, Notes, FollowUp, Contact, Stage, StageHistory


def open_opportunities(request):
    """Show open opportunities"""

    opportunities = Opportunity.objects.filter(open=True)

    return render(
        request,
        "opportunities.html",
        {"page_title": "Open Opportunities", "opportunities": opportunities},
    )
    
def all_opportunities(request):
    """Show all open opportunities, open and expired."""
    opportunities = Opportunity.objects.all().order_by("stage").order_by("company_name")
    return render(
        request,
        "opportunities.html",
        {"page_title": "All Opportunities", "opportunities": opportunities}
    )

def opportunity_view(request, opportunity_id):
    """Details about a specific opportunity"""
    opportunity = get_object_or_404(Opportunity, pk=opportunity_id)
    stages = Stage.objects.exclude(name__in=['Placeholder', opportunity.stage.name])    
    stage_transitions = StageHistory.objects.filter(opportunity=opportunity)
    notes = Notes.objects.filter(opportunity=opportunity)
    follow_ups = FollowUp.objects.filter(opportunity=opportunity)
    contacts = Contact.objects.filter(opportunity=opportunity)
    return render(
        request, "opportunity_detail.html", 
        {
            "page_title": "Opportunity Details", 
            "o": opportunity, 
            "stages": stages,
            "history": stage_transitions,
            "follow_ups": follow_ups,
            "contacts": contacts,
            "notes": notes}
    )

def update_opportunity_stage(request, opportunity_id, stage_id):
    opportunity = get_object_or_404(Opportunity, pk=opportunity_id)
    old_stage = opportunity.stage
    new_stage = get_object_or_404(Stage, pk=stage_id)

    # Track the change
    stage_transition = StageHistory()
    stage_transition.opportunity = opportunity
    stage_transition.new_stage = new_stage
    stage_transition.save()
    opportunity.stage = new_stage
    opportunity.save()
    return redirect("opportunity_view", opportunity_id=opportunity.id)




def opportunities_missing_contacts_follow_ups(request):
    opportunities = ( 
        Opportunity.objects.annotate(
            contact_count=Count("contact"), 
            note_count=Count("notes")
        ).filter(contact_count=0, note_count=0, open=True)
        .order_by("-initiation_date") 
    )
    return render(
        request, 
        "opportunities.html",
        {"page_title": "Opportunities missing Contacts and Follow Ups", "opportunities": opportunities}
    )

def all_contacts(request):
    contacts = Contact.objects.all()
    return render(request, "contacts.html", {"page_title": "All Contacts", "contacts": contacts})

def current_contacts(request):
    contacts = Contact.objects.filter(
        Q(opportunity=None) | Q(opportunity__open=True))
    return render(request, "contacts.html", {"page_title": "Current Contacts", "contacts": contacts})

def current_follow_ups(request):
    """Show all FollowUps for the next 7 days."""
    # follow_ups = FollowUp.objects.filter(follow_up_date__gte=datetime.date.today())
    follow_ups = FollowUp.objects.filter(
        Q(opportunity__open=True) & (
            Q(follow_up_date__gte=datetime.date.today()) |
            Q(completed=False)
        )
    ).order_by("follow_up_date")
    return render(
        request,
        "follow_ups.html",
        {"page_title": "Opportunities to Follow Up", "follow_ups": follow_ups}
    )

def complete_follow_up(request, follow_up_id):
    """
    Mark follow up as completed. Then go to Opportunity detail page
    
    :param request: Description
    :param follow_up_id: Description
    """
    follow_up = get_object_or_404(FollowUp, pk=follow_up_id)
    follow_up.completed = True
    follow_up.save()

    return redirect(opportunity_view, follow_up.opportunity.id)
