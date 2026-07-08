from django.test import TestCase
from django.db import IntegrityError
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
