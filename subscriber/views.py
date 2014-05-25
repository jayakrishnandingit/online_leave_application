from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from forms import SubscriberCreationForm
from client.forms import ClientForm
# Create your views here.
def register(request):
	context = {
		'user_creation_form' : UserCreationForm(),
		'subscriber_creation_form' : SubscriberCreationForm(),
		'client_form' : ClientForm()
	}
	return render(request, 'registration/registration.html', context)