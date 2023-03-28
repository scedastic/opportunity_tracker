from django.shortcuts import render
from .models import Opportunity, Notes, Contact


def dashboard(request):
    """Show open opportunities"""

    opportunities = Opportunity.objects.filter(open=True)

    return render(
        request,
        "dashboard.html",
        {"page_title": "Opportunities", "opportunities": opportunities},
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
    opportunities = Opportunity.objects.all()
    return render(
        request,
        "dashboard.html",
        {"page_title": "All Opportunities", "opportunities": opportunities}
    )
