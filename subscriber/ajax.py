from ola.common.ajax import JSONParser
from client.forms import ClientForm
from forms import SubscriberCreationForm
from models import Subscriber
from django.contrib.auth.forms import UserCreationForm

class SubscriberAjaxHandler(JSONParser):
	def do_registration(self, form_values):
		client_form = ClientForm(form_values)
		user_form = UserCreationForm(form_values)
		subscriber_form = SubscriberCreationForm(form_values)
		if client_form.is_valid() and user_form.is_valid() and subscriber_form.is_valid():
			client = client_form.save(commit=False)
			client.payment_status = 0 # no payment, not so far.
			client.save()
			user = user_form.save(commit=False)
			user.email = subscriber_form.cleaned_data['email']
			user.first_name = subscriber_form.cleaned_data['first_name']
			user.last_name = subscriber_form.cleaned_data['last_name']
			user.is_active = True
			user.is_staff = False
			user.save()
			subscriber = Subscriber(
				user=user,
				client=client,
				no_of_leave_remaining=0
			)
			subscriber.save()
			return self.respond(is_saved=True)
		return self.respond(
			is_saved=False, 
			client_form_errors=client_form.errors,
			user_form_errors=user_form.errors,
			subscriber_form_errors=subscriber_form.errors
		)