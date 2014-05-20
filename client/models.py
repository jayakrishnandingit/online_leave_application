from django.db import models

# Create your models here.
class Client(models.Model):
	name = models.CharField(max_length=100)
	created_on = models.DateTimeField(auto_now_add=True)
