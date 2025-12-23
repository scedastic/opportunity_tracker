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
from .views import all_opportunities, open_opportunities, opportunity_view, current_follow_ups

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", open_opportunities, name="open-opportunities"),
    path("opportunity/<int:opportunity_id>/", opportunity_view, name="opportunity_view"),
    path("all/", all_opportunities, name="all-opportunities"),
    path("followups/", current_follow_ups, name="current-follow-ups")
]
