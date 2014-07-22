from django.db import models
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe
from ola.common.models import BASIC_TYPES
from ola.common.config import BaseEnum
from django.contrib.auth.models import User
from client.models import Client, Team

# Create your models here.
class Subscriber(models.Model):
	user = models.ForeignKey(User, related_name='subscriber_user')
	client = models.ForeignKey(Client, related_name='subscriber_client')
	created_on = models.DateTimeField(auto_now_add=True)
	maxDepth = 1

	def __unicode__(self):
		return u'%s' % self.name

	@property
	def name(self):
		return '%s' % self.user.get_full_name()

	@property
	def showGroup(self):
		if not self.user.is_superuser:
			userGroups = self.user.groups.get()
			return {
				'name' : userGroups.name,
				'id' : userGroups.id
			}
		return 'Admin'

	def get_absolute_url(self):
		return reverse('subscriber_details', args=[str(self.user.id)])

	@property
	def profile_url(self):
		return mark_safe('<a class="profile_link" href="%s">%s</a>' % (self.get_absolute_url(), self.name))

	def serialize(self, maxDepth=1, requestPassword=False):
		import datetime
		from django.contrib.auth.models import User
		from ola.settings import DATETIME_INPUT_FORMATS, DATE_INPUT_FORMATS

		output = {}

		for prop in self._meta.get_all_field_names():
			value = getattr(self, prop)
			if value is None or isinstance(value, BASIC_TYPES):
				output[prop] = value
			elif isinstance(value, datetime.datetime):
				output[prop] = value.strftime(DATETIME_INPUT_FORMATS[0])
			elif isinstance(value, datetime.date):
				output[prop] = value.strftime(DATE_INPUT_FORMATS[0])
			elif isinstance(value, User):
				output[prop] = self._user(value, requestPassword)
			elif isinstance(value, models.Model):
				if self.maxDepth <= maxDepth:
					output[prop] = value.serialize((maxDepth - 1))
				else:
					output[prop] = value.id
			else:
				pass
		output['group'] = self.showGroup
		output['profile_path'] = self.get_absolute_url()
		output['profile_url'] = self.profile_url
		output['name'] = self.name
		return output

	def _user(self, value, requestPassword):
		return {
			'id' : value.id,
			'username' : value.username,
			'password' : value.password if requestPassword else None,
			'first_name' : value.first_name,
			'last_name' : value.last_name,
			'name' : value.get_full_name(),
			'email' : value.email,
			'is_superuser' : value.is_superuser,
			'is_staff' : value.is_staff,
			'is_active' : value.is_active
		}

class NotificationActionEnum(BaseEnum):
	def __init__(self, *args, **kwargs):
		self.LEAVE_REQUESTED = 0
		self.LEAVE_APPROVED = 1
		self.LEAVE_DENIED = 2

NotificationAction = NotificationActionEnum()

NOTIFICATION_ACTION_LABEL = {
	NotificationAction.LEAVE_REQUESTED : 'Leave Requested',
	NotificationAction.LEAVE_APPROVED : 'Leave Approved',
	NotificationAction.LEAVE_DENIED : 'Leave Denied',
}

class SubscriberNotification(models.Model):
	actor = models.ForeignKey(Subscriber, related_name='notification_actor')
	action = models.IntegerField()
	recipient = models.ForeignKey(Subscriber, related_name='notification_recipient')
	has_read = models.BooleanField(default=False)
	created_on = models.DateTimeField(auto_now_add=True)
	updated_on = models.DateTimeField(auto_now=True)
	maxDepth = 1

	def serialize(self, maxDepth=1, requestPassword=False):
		import datetime
		from django.contrib.auth.models import User
		from ola.settings import DATETIME_INPUT_FORMATS, DATE_INPUT_FORMATS

		output = {}

		for prop in self._meta.get_all_field_names():
			value = getattr(self, prop)
			if value is None or isinstance(value, BASIC_TYPES):
				output[prop] = value
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