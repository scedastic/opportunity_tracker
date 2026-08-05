from datetime import date

from django.test import TestCase
from django.db import IntegrityError
from django.urls import reverse

from .models import Company, Opportunity, Contact, Stage


class ContactOpportunityManyToManyTests(TestCase):
    def setUp(self):
        self.stage = Stage.objects.create(name="Applied", rank=1)
        self.company = Company.objects.create(name="Acme")
        self.opportunity1 = Opportunity.objects.create(
            company_name="Acme",
            company=self.company,
            stack="Python",
            requirements="Django",
            stage=self.stage,
        )
        self.opportunity2 = Opportunity.objects.create(
            company_name="Acme",
            company=self.company,
            stack="Python",
            requirements="Django",
            stage=self.stage,
        )
        self.contact = Contact.objects.create(name="Jane")

    def test_contact_can_be_linked_to_multiple_opportunities(self):
        self.contact.opportunities.add(self.opportunity1, self.opportunity2)

        self.assertEqual(self.contact.opportunities.count(), 2)
        self.assertEqual(self.opportunity1.contacts.count(), 1)
        self.assertEqual(self.opportunity2.contacts.count(), 1)

    def test_contact_can_exist_without_opportunities(self):
        self.assertEqual(self.contact.opportunities.count(), 0)


class StageSummaryViewTests(TestCase):
    def test_stage_summary_lists_counts_and_percentages(self):
        applied_stage = Stage.objects.create(name="Applied", rank=1)
        interview_stage = Stage.objects.create(name="Interview", rank=2)
        placeholder_stage = Stage.objects.create(name="Placeholder", rank=99)

        company = Company.objects.create(name="Test Co")
        Opportunity.objects.create(
            company_name="Test Co",
            company=company,
            stack="Python",
            requirements="Django",
            stage=applied_stage,
        )
        Opportunity.objects.create(
            company_name="Test Co",
            company=company,
            stack="Python",
            requirements="Django",
            stage=applied_stage,
        )
        Opportunity.objects.create(
            company_name="Test Co",
            company=company,
            stack="Python",
            requirements="Django",
            stage=interview_stage,
        )
        Opportunity.objects.create(
            company_name="Test Co",
            company=company,
            stack="Python",
            requirements="Django",
            stage=placeholder_stage,
        )

        response = self.client.get(reverse("stage-summary"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["total_opportunities"], 3)
        self.assertEqual(response.context["stage_summary"][0]["name"], "Applied")
        self.assertEqual(response.context["stage_summary"][0]["count"], 2)
        self.assertEqual(response.context["stage_summary"][0]["percentage"], 66.7)
        self.assertEqual(response.context["stage_summary"][1]["name"], "Interview")
        self.assertEqual(response.context["stage_summary"][1]["count"], 1)
        self.assertEqual(response.context["stage_summary"][1]["percentage"], 33.3)


class OpportunitySortingTests(TestCase):
    def setUp(self):
        self.applied_stage = Stage.objects.create(name="Applied", rank=1)
        self.rejected_stage = Stage.objects.create(name="Rejected", rank=2)

    def test_open_opportunities_can_be_sorted_by_date_descending(self):
        older_opportunity = Opportunity.objects.create(
            company_name="Zeta",
            company=Company.objects.create(name="Zeta"),
            stack="Python",
            requirements="Django",
            stage=self.applied_stage,
            initiation_date=date(2024, 1, 1),
        )
        newer_opportunity = Opportunity.objects.create(
            company_name="Alpha",
            company=Company.objects.create(name="Alpha"),
            stack="Python",
            requirements="Django",
            stage=self.applied_stage,
            initiation_date=date(2024, 2, 1),
        )
        Opportunity.objects.create(
            company_name="Hidden",
            company=Company.objects.create(name="Hidden"),
            stack="Python",
            requirements="Django",
            stage=self.rejected_stage,
            initiation_date=date(2024, 3, 1),
        )

        response = self.client.get(reverse("open-opportunities"), {"sort_by": "date", "sort_order": "desc"})

        self.assertEqual(response.context["current_sort_by"], "date")
        self.assertEqual(response.context["current_sort_order"], "desc")
        self.assertEqual(list(response.context["opportunities"]), [newer_opportunity, older_opportunity])

    def test_all_opportunities_can_be_sorted_by_company_name_ascending(self):
        beta_company = Company.objects.create(name="Beta")
        alpha_company = Company.objects.create(name="Alpha")
        beta_opportunity = Opportunity.objects.create(
            company_name="Beta",
            company=beta_company,
            stack="Python",
            requirements="Django",
            stage=self.applied_stage,
        )
        alpha_opportunity = Opportunity.objects.create(
            company_name="Alpha",
            company=alpha_company,
            stack="Python",
            requirements="Django",
            stage=self.applied_stage,
        )

        response = self.client.get(reverse("all-opportunities"), {"sort_by": "company_name", "sort_order": "asc"})

        self.assertEqual(response.context["current_sort_by"], "company_name")
        self.assertEqual(response.context["current_sort_order"], "asc")
        self.assertEqual(list(response.context["opportunities"]), [alpha_opportunity, beta_opportunity])
