from django.db import models
from ola.common.models import BASIC_TYPES
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