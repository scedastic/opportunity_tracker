import datetime
from django.db.models import Q
from django.shortcuts import get_object_or_404, render
from .models import Opportunity, Notes, FollowUp, Contact


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
    opportunities = Opportunity.objects.all().order_by("stage")
    return render(
        request,
        "opportunities.html",
        {"page_title": "All Opportunities", "opportunities": opportunities}
    )

def opportunity_view(request, opportunity_id):
    """Details about a specific opportunity"""
    opportunity = get_object_or_404(Opportunity, pk=opportunity_id)
    notes = Notes.objects.filter(opportunity=opportunity)
    return render(
        request, "opportunity_detail.html", {"o": opportunity, "notes": notes}
    )


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