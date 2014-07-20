import datetime
import decimal
from django.db import models
from ola.common.models import BASIC_TYPES
from ola.common.config import BaseEnum
from client.models import Client, Team
from subscriber.models import Subscriber
from ola.settings import DATETIME_INPUT_FORMATS, DATE_INPUT_FORMATS

# Create your models here.
class LeaveType(models.Model):
	type_of_leave = models.CharField(max_length=100)
	no_of_leave = models.IntegerField()
	# carry_forward_percentage
	# max_leave_allowed
	client = models.ForeignKey(Client, related_name='leave_type_client')
	created_on = models.DateTimeField(auto_now_add=True)
	created_by = models.ForeignKey(Subscriber, related_name='leave_type_subscriber')
	maxDepth = 1

	def serialize(self, maxDepth=1):
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

class LeaveBucket(models.Model):
	subscriber = models.ForeignKey(Subscriber, related_name='subscriber_leave_bucket_subscriber')
	type_of_leave = models.ForeignKey(LeaveType, related_name='subscriber_leave_bucket_type')
	bucket = models.FloatField()
	created_on = models.DateTimeField(auto_now_add=True)
	created_by = models.ForeignKey(Subscriber, related_name='subscriber_leave_bucket_created_by')
	updated_on = models.DateTimeField(auto_now=True)
	maxDepth = 1

	def serialize(self, maxDepth=1):
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

class LeaveStatusEnum(BaseEnum):
	def __init__(self, *args, **kwargs):
		self.PENDING = 0
		self.APPROVED = 1
		self.DENIED = 2

LeaveStatus = LeaveStatusEnum()

LEAVE_STATUS_LABEL = {
	LeaveStatus.PENDING : 'Pending Approval',
	LeaveStatus.APPROVED : 'Approved',
	LeaveStatus.DENIED : 'Denied',
}

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

	def period(self):
		return '%s - %s' % (self.start.strftime(DATETIME_INPUT_FORMATS[0]), self.end.strftime(DATETIME_INPUT_FORMATS[0]))

	def serialize(self, maxDepth=1):
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
		output['period'] = self.period()
		return output
