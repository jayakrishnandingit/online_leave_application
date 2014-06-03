from django.db import models
from ola.common.models import BASIC_TYPES

# Create your models here.
class Client(models.Model):
	name = models.CharField(max_length=100)
	payment_status = models.IntegerField()
	created_on = models.DateTimeField(auto_now_add=True)
	maxDepth = 1

	def serialize(self, maxDepth=1):
		import datetime
		import decimal
		from ola.settings import DATETIME_INPUT_FORMATS, DATE_INPUT_FORMATS

		output = {}

		for prop in self._meta.get_all_field_names():
			value = getattr(self, prop)
			if value is None or isinstance(value, BASIC_TYPES):
				output[prop] = value
			elif isinstance(value, decimal.Decimal):
				# TODO: we need to find a work around for this
				output[prop] = float(value)
			elif isinstance(value, datetime.datetime):
				output[prop] = value.strftime(DATETIME_INPUT_FORMATS[0])
			elif isinstance(value, datetime.date):
				output[prop] = value.strftime(DATE_INPUT_FORMATS[0])
			elif isinstance(value, models.Model):
				if self.maxDepth <= maxDepth:
					output[prop] = value.serialize((maxDepth - 1))
				else:
					output[prop] = value.id
			else:
				pass

		return output

class Team(models.Model):
	name = models.CharField(max_length=100)
	client = models.ForeignKey(Client, related_name='team_client')
	created_on = models.DateTimeField(auto_now_add=True)
	maxDepth = 1

	def serialize(self, maxDepth=1):
		import datetime
		import decimal
		from ola.settings import DATETIME_INPUT_FORMATS, DATE_INPUT_FORMATS

		output = {}

		for prop in self._meta.get_all_field_names():
			value = getattr(self, prop)
			if value is None or isinstance(value, BASIC_TYPES):
				output[prop] = value
			elif isinstance(value, decimal.Decimal):
				# TODO: we need to find a work around for this
				output[prop] = float(value)
			elif isinstance(value, datetime.datetime):
				output[prop] = value.strftime(DATETIME_INPUT_FORMATS[0])
			elif isinstance(value, datetime.date):
				output[prop] = value.strftime(DATE_INPUT_FORMATS[0])
			elif isinstance(value, models.Model):
				if self.maxDepth <= maxDepth:
					output[prop] = value.serialize((maxDepth - 1))
				else:
					output[prop] = value.id
			else:
				pass

		return output
