from django.db import models
from django.contrib.auth.models import User
from client.models import Client, Team

# Create your models here.
class Subscriber(models.Model):
	user = models.ForeignKey(User, related_name='subscriber_user')
	client = models.ForeignKey(Client, related_name='subscriber_client')
	# initialized to no leaves as to the leave policy for the client
	# this must be updated each time a leave gets approved.
	no_of_leave_remaining = models.IntegerField()
	created_on = models.DateTimeField(auto_now_add=True)
