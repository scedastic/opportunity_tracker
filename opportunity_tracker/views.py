from django.shortcuts import render
from .models import Opportunity, Notes, Contact


def dashboard(request):
    opportunities = Opportunity.objects.filter(open=True)

    return render(
        request,
        "dashboard.html",
        {"page_title": "Opportunities", "opportunities": opportunities},
    )
