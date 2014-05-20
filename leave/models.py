from django.db import models

# Create your models here.
class LeaveType(models.Model):
	from subscriber.models import Subscriber
	from client.models import Client

	type_of_leave = models.CharField(max_length=100)
	client = models.ForeignKey(Client, related_name='leave_type_client')
	created_on = models.DateTimeField(auto_now_add=True)
	created_by = models.ForeignKey(Subscriber, related_name='leave_type_subscriber')

class Holiday(models.Model):
	from subscriber.models import Subscriber

	name = models.CharField(max_length=100)
	start = models.DateField()
	end = models.DateField()
	created_on = models.DateTimeField(auto_now_add=True)
	created_by = models.ForeignKey(Subscriber, related_name='holiday_subscriber')

class LeavePolicy(models.Model):
	from subscriber.models import Subscriber, Team

	type_of_leave = models.ManyToManyField(LeaveType, related_name='leave_policy_leave_type_m2m')
	no_of_leave = models.IntegerField()
	start = models.DateTimeField()
	end = models.DateTimeField()
	team = models.ManyToManyField(Team, related_name='leave_policy_team')
	is_disabled = models.BooleanField(default=False)
	created_on = models.DateTimeField(auto_now_add=True)
	created_by = models.ForeignKey(Subscriber, related_name='leave_policy_subscriber')

class Leave(models.Model):
	from subscriber.models import Subscriber

	start = models.DateTimeField()
	end = models.DateTimeField()
	# this will be pulled from user group @see SubscriberGroup
	type_of_leave = models.ForeignKey(LeaveType, related_name='leave_leave_type')
	# this will be automatically updated when saving.
	no_leave_remaining = models.IntegerField()
	requester = models.ForeignKey(Subscriber, related_name='leave_requester')
	approver = models.ForeignKey(Subscriber, related_name='leave_approver')
	status = models.IntegerField()
	created_on = models.DateTimeField(auto_now_add=True)
