from django.db import models
from phone_field import PhoneField


class Stage(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=25)
    rank = models.IntegerField()

    def __str__(self):
        return f"{self.name}"
    
    class Meta:
        ordering = ["rank"]


class Opportunity(models.Model):
    id = models.AutoField(primary_key=True)
    company_name = models.CharField(max_length=50, db_index=True)
    posted_minimum = models.IntegerField(default=0)
    stack = models.CharField(max_length=50, db_index=True)
    requirements = models.CharField(max_length=255, db_index=True)
    open = models.BooleanField(default=True)
    stage = models.ForeignKey(Stage, on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.company_name} {self.stack}  ${self.posted_minimum}"

    class Meta:
        verbose_name_plural = "Opportunities"
        ordering = ["company_name"]


class Notes(models.Model):
    id = models.AutoField(primary_key=True)
    opportunity = models.ForeignKey(Opportunity, on_delete=models.CASCADE)
    date = models.DateField()
    note = models.TextField()

    def __str__(self):
        return f"{self.opportunity.company_name} Note: {self.date}"

    class Meta:
        verbose_name_plural = "Notes"
        ordering = ["opportunity"]


class Contact(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    phone = PhoneField(blank=True, help_text="Contact phone number")
    email = models.EmailField(max_length=255, blank=True)
    opportunity = models.ForeignKey(Opportunity, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.name} {self.phone } @ {self.opportunity.company_name}"

    class Meta:
        ordering = ["name"]
