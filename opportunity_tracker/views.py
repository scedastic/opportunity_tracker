import datetime
from django.shortcuts import render
from .models import Opportunity, Notes, FollowUp, Contact


def dashboard(request):
    """Show open opportunities"""

    opportunities = Opportunity.objects.filter(open=True)

    return render(
        request,
        "dashboard.html",
        {"page_title": "Open Opportunities", "opportunities": opportunities},
    )


def opportunity_view(request, opportunity_id):
    """Details about a specific opportunity"""
    opportunity = Opportunity.objects.get(pk=opportunity_id)
    notes = Notes.objects.filter(opportunity=opportunity)
    return render(
        request, "opportunity_detail.html", {"o": opportunity, "notes": notes}
    )
    
def all_opportunities(request):
    """Show all open opportunities, open and expired."""
    opportunities = Opportunity.objects.all().order_by("stage")
    return render(
        request,
        "dashboard.html",
        {"page_title": "All Opportunities", "opportunities": opportunities}
    )

def current_follow_ups(request):
    """Show all FollowUps for the next 7 days."""
    follow_ups = FollowUp.objects.filter(follow_up_date__gte=datetime.date.today())
    return render(
        request,
        "follow_ups.html",
        {"page_title": "Opportunities to Follow Up", "follow_ups": follow_ups}
    )