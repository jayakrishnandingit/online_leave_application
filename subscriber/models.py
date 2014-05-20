from django.db import models

# Create your models here.
class Team(models.Model):
	from client.models import Client

	name = models.CharField(max_length=100)
	client = models.ForeignKey(Client, related_name='team_client')
	created_on = models.DateTimeField(auto_now_add=True)

class Subscriber(models.Model):
	from django.contrib.auth.models import User
	from client.models import Client

	user = models.ForeignKey(User, related_name='subscriber_user')
	client = models.ForeignKey(Client, related_name='subscriber_client')
	team = models.ForeignKey(Team, related_name='subscriber_team')
	created_on = models.DateTimeField(auto_now_add=True)
