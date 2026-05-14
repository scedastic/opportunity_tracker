from django.db import models
from django.db.models.functions import Upper
from phone_field import PhoneField
import datetime

class Stage(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=25)
    rank = models.IntegerField()

    def __str__(self):
        return f"{self.name}"
    
    class Meta:
        ordering = ["rank"]

class Company(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, db_index=True)
    is_recruiter = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name}"
    
    class Meta:
        verbose_name_plural = "Companies"
        ordering = [Upper("name")]


class Opportunity(models.Model):
    id = models.AutoField(primary_key=True)
    company_name = models.CharField(max_length=50, db_index=True, null=True, blank=True)
    company = models.ForeignKey(Company, on_delete=models.PROTECT, default=202)
    job_title = models.CharField(max_length=50, default="SOFTWARE")
    posted_minimum = models.IntegerField(default=0)
    posted_maximum = models.IntegerField(default=0)
    stack = models.CharField(max_length=50, db_index=True)
    requirements = models.CharField(max_length=255, db_index=True)
    stage = models.ForeignKey(Stage, on_delete=models.PROTECT)
    initiation_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return_str = f"{self.company} {self.job_title}"
        if self.posted_minimum > 0: 
            return_str += f" ${self.posted_minimum}"
        return return_str + f" - {self.stage} {self.initiation_date}"

    class Meta:
        verbose_name_plural = "Opportunities"
        ordering = [Upper("company_name")]


class StageHistory(models.Model):
    id = models.AutoField(primary_key=True)
    opportunity = models.ForeignKey(Opportunity, on_delete=models.CASCADE)
    new_stage = models.ForeignKey(Stage, on_delete=models.PROTECT)
    transition_date = models.DateField(default=datetime.datetime.today)

    class Meta:
        verbose_name_plural = "Stage History"
        ordering=["transition_date"]


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
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        if self.opportunity is None:
            return f"{self.name} {self.phone}"
        else:
            return f"{self.name} {self.phone} @ {self.opportunity.company_name}"

    class Meta:
        ordering = [Upper("name")]

class FollowUp(models.Model):
    id = models.AutoField(primary_key=True)
    opportunity = models.ForeignKey(Opportunity, on_delete=models.SET_NULL, null=True, blank=True)
    contact = models.ForeignKey(Contact, on_delete=models.SET_NULL, null=True, blank=True)
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True, blank=True)
    follow_up_date = models.DateField(blank=True, null=True)
    completed = models.BooleanField(default=False)

    def __str__(self):
        if self.opportunity is None:
            return f"{self.follow_up_date}"
        return f"{self.follow_up_date} - {self.opportunity}"

    class Meta:
        ordering = ["follow_up_date"]   