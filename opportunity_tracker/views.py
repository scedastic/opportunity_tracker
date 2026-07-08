import datetime
from urllib import request, response
from django.db.models import Q, Count
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CompanyForm, FollowUpForm, NoteForm, OpportunityForm
from .models import Company, Opportunity, Notes, FollowUp, Contact, Stage, StageHistory

##################
# Frontend views #
##################
def dashboard(request):
    return render(request, "dashboard.html", {"page_title": "Dashboard"})

def add_company(request):
    if request.method == "POST":
        form = CompanyForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("dashboard")
    else:
        context = {}
        context["form"] = CompanyForm()
    return render(request, "add_company.html", {"form": CompanyForm})

def company_view(request, company_id):
    """Show all opportunities for a given company."""
    opportunities = Opportunity.objects.filter(company_id=company_id).order_by("stage")
    company_name = opportunities.first().company_name if opportunities.exists() else "Unknown Company"
    return render(
        request,
        "opportunities.html",
        {"page_title": f"Opportunities at {company_name}", "opportunities": opportunities},
    )

def all_companies(request):
    """Show all companies."""
    companies = Company.objects.annotate(
        in_play=Count(
            "opportunity",
            filter=Q(
                opportunity__stage__name="Sent Resume"
            ) | Q(
                opportunity__stage__name__icontains="interview"
            ),
        )
    ).order_by("name")
    return render(
        request,
        "companies.html",
        {"page_title": "All Companies", "companies": companies},
    )

def open_opportunities(request):
    """Show open opportunities"""

    opportunities = Opportunity.objects.filter(stage__name__in=[
        "Sent Resume",
        "HR Interview",
        "Technical Interview",]).order_by("company")
    return render(
        request,
        "opportunities.html",
        {"page_title": "Open Opportunities", "opportunities": opportunities},
    )
    
def all_opportunities(request):
    """Show all open opportunities, regardless of stage."""
    opportunities = Opportunity.objects.all().order_by("stage").order_by("company")
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
    contacts = Contact.objects.filter(opportunities=opportunity)
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
    if opportunity.stage == "Abandoned":
        return redirect("open-opportunities")
    return redirect("opportunity_view", opportunity_id=opportunity.id)

def add_opportunity(request):
    if request.method == "POST":
        print("POSTING!")
        form = OpportunityForm(request.POST)
        if form.is_valid():
            print("VALID!")
            # if posted maximum is not filled in, then set it to the posted minimum. 
            # form.posted_maximum = max(form.posted_maximum, form.posted_minimum)
            form.save()
            new_stage_history = StageHistory()
            new_stage_history.opportunity = form.instance
            new_stage_history.new_stage = form.instance.stage
            new_stage_history.transition_date = datetime.date.today()
            new_stage_history.save()            
            return redirect("open-opportunities")
        else:   # Debugging only
            print("not valid")
    else:
        print("not posting")
        context = {}
        context["form"] = OpportunityForm()
    return render(request, "opportunity.html", {"form": OpportunityForm})

def add_notes_to_opportunity(request, opportunity_id):
    opportunity = get_object_or_404(Opportunity, pk=opportunity_id)
    if request.method == "POST":
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.opportunity = opportunity
            note.save()
            return redirect("opportunity_view", opportunity_id=opportunity_id)
    else:
        context = {}
        context["page_title"] = "Add Note to Opportunity - " + opportunity.job_title
        form = NoteForm()
        form.fields["opportunity"].initial = opportunity
        context["form"] = form
    return render(request, "add_note.html", context)
    pass

def opportunities_missing_contacts_follow_ups(request):
    opportunities = ( 
        Opportunity.objects.annotate(
            contact_count=Count("contacts"), 
            note_count=Count("notes")
        ).filter(contact_count=0, note_count=0)
        .order_by("-initiation_date") 
    )
    return render(
        request, 
        "opportunities.html",
        {"page_title": "Opportunities missing Contacts and Follow Ups", "opportunities": opportunities}
    )

def recruiters(request):
    recruiters = Company.objects.filter(is_recruiter=True)
    contacts = Contact.objects.filter(company__in=recruiters).order_by("company")
    context = {"page_title": "Recruiters", "recruiters": recruiters, "contacts": contacts}
    return render(request, "recruiters.html", context)

def all_contacts(request):
    contacts = Contact.objects.all()
    return render(request, "contacts.html", {"page_title": "All Contacts", "contacts": contacts})

# View may not be relevant.
def current_contacts(request):
    contacts = Contact.objects.filter(opportunities__isnull=True).distinct()
    return render(request, "contacts.html", {"page_title": "Current Contacts", "contacts": contacts})

def current_follow_ups(request):
    """Show all FollowUps for the next 7 days."""
    # follow_ups = FollowUp.objects.filter(follow_up_date__gte=datetime.date.today())
    follow_ups = FollowUp.objects.filter(
        Q(follow_up_date__gte=datetime.date.today()) |
        Q(completed=False)        
    ).order_by("follow_up_date")
    return render(
        request,
        "follow_ups.html",
        {"page_title": "Opportunities to Follow Up", "follow_ups": follow_ups}
    )

def add_follow_up(request, opportunity_id):
    opportunity = get_object_or_404(Opportunity, pk=opportunity_id)
    if request.method == "POST":
        form = FollowUpForm(request.POST)
        if form.is_valid():
            follow_up = form.save(commit=False)
            follow_up.opportunity = opportunity
            follow_up.completed = False
            follow_up.save()
            return redirect("opportunity_view", opportunity_id=opportunity_id)
    else:
        context = {}
        context["page_title"] = f"Add Follow Up for {opportunity.company_name}"
        form = FollowUpForm()
        form.fields["opportunity"].initial = opportunity
        context["form"] = form        
    return render(request, "add_follow_up.html", context)

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
