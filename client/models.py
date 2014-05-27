from django.db import models

# Create your models here.
class Client(models.Model):
	name = models.CharField(max_length=100)
	payment_status = models.IntegerField()
	created_on = models.DateTimeField(auto_now_add=True)

class Team(models.Model):
	name = models.CharField(max_length=100)
	client = models.ForeignKey(Client, related_name='team_client')
	created_on = models.DateTimeField(auto_now_add=True)
