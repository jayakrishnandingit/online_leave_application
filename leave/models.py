from django.db import models
from client.models import Client, Team
from subscriber.models import Subscriber

# Create your models here.
class LeaveType(models.Model):
	type_of_leave = models.CharField(max_length=100)
	client = models.ForeignKey(Client, related_name='leave_type_client')
	created_on = models.DateTimeField(auto_now_add=True)
	created_by = models.ForeignKey(Subscriber, related_name='leave_type_subscriber')

class Holiday(models.Model):
	name = models.CharField(max_length=100)
	start = models.DateField()
	end = models.DateField()
	client = models.ForeignKey(Client, related_name='holiday_client')
	created_on = models.DateTimeField(auto_now_add=True)
	created_by = models.ForeignKey(Subscriber, related_name='holiday_subscriber')

class LeavePolicy(models.Model):
	type_of_leave = models.ManyToManyField(LeaveType, related_name='leave_policy_leave_type_m2m')
	no_of_leave = models.IntegerField()
	start = models.DateTimeField()
	end = models.DateTimeField()
	client = models.ForeignKey(Client, related_name='leave_policy_client')
	is_disabled = models.BooleanField(default=False)
	created_on = models.DateTimeField(auto_now_add=True)
	created_by = models.ForeignKey(Subscriber, related_name='leave_policy_subscriber')

class Leave(models.Model):
	start = models.DateTimeField()
	end = models.DateTimeField()
	type_of_leave = models.ForeignKey(LeaveType, related_name='leave_leave_type')
	requester = models.ForeignKey(Subscriber, related_name='leave_requester')
	approver = models.ForeignKey(Subscriber, related_name='leave_approver')
	status = models.IntegerField()
	comments = models.TextField(null=True)
	created_on = models.DateTimeField(auto_now_add=True)
