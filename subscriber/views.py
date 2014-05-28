import json
from django import http
from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from ola.common.utils import get_value_from_request
from forms import SubscriberCreationForm
from client.forms import ClientForm
from subscriber.ajax import SubscriberAjaxHandler
from django.views.generic import View

# Create your views here.
def register(request):
	context = {
		'user_creation_form' : UserCreationForm(),
		'subscriber_creation_form' : SubscriberCreationForm(),
		'client_form' : ClientForm()
	}
	return render(request, 'registration/registration.html', context)

class SubscriberView(View):
	def get(self, request):
		raise NotImplementedError

	def post(self, request):
		args = json.loads(request.body)
		ajaxMainClass = SubscriberAjaxHandler()
		ajaxMainClass.httpRequest = request
		ajaxMainClass.user = request.user
		funtionToCall = getattr(ajaxMainClass, args.pop(), None)
		if not funtionToCall:
			return http.Http404

		responseValues = funtionToCall(*args)
		response = http.HttpResponse()
		response.status_code = 200
		response.write(responseValues)
		response['Content-Type'] = 'application/json'
		return response

class SubscriberDetailsView(View):
	pass
