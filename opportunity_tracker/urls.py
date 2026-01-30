"""opportunity_tracker URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from .views import (
    all_opportunities, open_opportunities, opportunities_missing_contacts_follow_ups, 
    opportunity_view, update_opportunity_stage,
    all_contacts, current_contacts,
    current_follow_ups, complete_follow_up,
    )

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", open_opportunities, name="open-opportunities"),
    path("opportunity/<int:opportunity_id>/", opportunity_view, name="opportunity_view"),
    path("opportunity/<int:opportunity_id>/update-stage/<int:stage_id>/", update_opportunity_stage, name="update-opportunity-stage"),
    path("all/", all_opportunities, name="all-opportunities"),
    path("contacts/", all_contacts, name="all-contacts"),
    path("current-contacts/", current_contacts, name="current-contacts"),
    path("opp-no-cf/", opportunities_missing_contacts_follow_ups, name="opportunites-without-contacts-follow-ups"),
    path("followups/", current_follow_ups, name="current-follow-ups"),
    path("follow-up/<int:follow_up_id>/completed/", complete_follow_up, name="complete-follow-up"),
]
