from datetime import date

from django.test import TestCase
from django.db import IntegrityError
from django.urls import reverse

from .models import Company, Contact, ContactConstantly, FollowUp, Opportunity, Stage, StageHistory


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


class CompanyCheckViewTests(TestCase):
    def test_check_company_shows_form_without_a_result(self):
        response = self.client.get(reverse("check-company"))

        self.assertEqual(response.status_code, 200)
        self.assertIsNone(response.context["company_exists"])

    def test_check_company_finds_name_case_insensitively(self):
        company = Company.objects.create(name="Acme")

        response = self.client.post(reverse("check-company"), {"name": " acme "})

        self.assertTrue(response.context["company_exists"])
        self.assertEqual(response.context["company_id"], company.id)
        self.assertContains(response, f"acme exists in the database with ID {company.id}.")

    def test_check_company_reports_missing_name(self):
        response = self.client.post(reverse("check-company"), {"name": "Unknown Co"})

        self.assertFalse(response.context["company_exists"])
        self.assertContains(response, "Unknown Co does not exist in the database.")
        self.assertContains(response, "Add Company")
        self.assertContains(response, "?name=Unknown%20Co")

    def test_add_company_prefills_name_from_query_string(self):
        response = self.client.get(reverse("add-company"), {"name": "Unknown Co"})

        self.assertEqual(response.context["form"].initial["name"], "Unknown Co")


class ContactConstantlyViewTests(TestCase):
    def test_lists_contact_constantly_contacts_and_logs_completed_follow_up(self):
        frequent_contact = Contact.objects.create(name="Jane")
        other_contact = Contact.objects.create(name="John")
        ContactConstantly.objects.create(contact=frequent_contact)

        response = self.client.get(reverse("contact-constantly"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["contacts"]), [frequent_contact])
        self.assertContains(response, frequent_contact.name)
        self.assertNotContains(response, other_contact.name)

        response = self.client.post(
            reverse("complete-contact-constantly", args=[frequent_contact.id])
        )

        self.assertRedirects(response, reverse("contact-constantly"))
        follow_up = FollowUp.objects.get(contact=frequent_contact)
        self.assertEqual(follow_up.follow_up_date, date.today())
        self.assertTrue(follow_up.completed)

    def test_cannot_log_follow_up_for_contact_not_marked_contact_constantly(self):
        contact = Contact.objects.create(name="Jane")

        self.client.post(reverse("complete-contact-constantly", args=[contact.id]))

        self.assertFalse(FollowUp.objects.filter(contact=contact).exists())


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


class RejectedOpportunitiesViewTests(TestCase):
    def test_lists_rejected_opportunities_with_time_to_rejection(self):
        applied_stage = Stage.objects.create(name="Applied", rank=1)
        rejected_stage = Stage.objects.create(name="Rejected - No Fit", rank=2)
        company = Company.objects.create(name="Acme")
        rejected_opportunity = Opportunity.objects.create(
            company=company,
            job_title="Backend Developer",
            stack="Python",
            requirements="Django",
            stage=rejected_stage,
            initiation_date=date(2024, 1, 1),
        )
        StageHistory.objects.create(
            opportunity=rejected_opportunity,
            new_stage=applied_stage,
            transition_date=date(2024, 1, 1),
        )
        StageHistory.objects.create(
            opportunity=rejected_opportunity,
            new_stage=rejected_stage,
            transition_date=date(2024, 1, 15),
        )
        active_opportunity = Opportunity.objects.create(
            company=company,
            job_title="Frontend Developer",
            stack="JavaScript",
            requirements="React",
            stage=applied_stage,
            initiation_date=date(2024, 1, 1),
        )

        response = self.client.get(reverse("rejected-opportunities"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["records_count"], 1)
        listed_opportunity = response.context["opportunities"][0]
        self.assertEqual(listed_opportunity, rejected_opportunity)
        self.assertEqual(listed_opportunity.rejection_date, date(2024, 1, 15))
        self.assertEqual(listed_opportunity.days_to_rejection, 14)
        self.assertNotContains(response, active_opportunity.job_title)
