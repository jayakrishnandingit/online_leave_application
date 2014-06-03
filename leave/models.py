from django.db import models
from ola.common.models import BASIC_TYPES
from client.models import Client, Team
from subscriber.models import Subscriber

# Create your models here.
class LeaveType(models.Model):
	type_of_leave = models.CharField(max_length=100)
	client = models.ForeignKey(Client, related_name='leave_type_client')
	created_on = models.DateTimeField(auto_now_add=True)
	created_by = models.ForeignKey(Subscriber, related_name='leave_type_subscriber')
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


class Holiday(models.Model):
	name = models.CharField(max_length=100)
	start = models.DateField()
	end = models.DateField()
	client = models.ForeignKey(Client, related_name='holiday_client')
	created_on = models.DateTimeField(auto_now_add=True)
	created_by = models.ForeignKey(Subscriber, related_name='holiday_subscriber')
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


class LeavePolicy(models.Model):
	type_of_leave = models.ManyToManyField(LeaveType, related_name='leave_policy_leave_type_m2m')
	no_of_leave = models.IntegerField()
	start = models.DateTimeField()
	end = models.DateTimeField()
	client = models.ForeignKey(Client, related_name='leave_policy_client')
	is_disabled = models.BooleanField(default=False)
	created_on = models.DateTimeField(auto_now_add=True)
	created_by = models.ForeignKey(Subscriber, related_name='leave_policy_subscriber')
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


class Leave(models.Model):
	start = models.DateTimeField()
	end = models.DateTimeField()
	type_of_leave = models.ForeignKey(LeaveType, related_name='leave_leave_type')
	requester = models.ForeignKey(Subscriber, related_name='leave_requester')
	approver = models.ForeignKey(Subscriber, related_name='leave_approver')
	status = models.IntegerField()
	comments = models.TextField(null=True)
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

