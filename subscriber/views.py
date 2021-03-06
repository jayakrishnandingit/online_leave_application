import json
from django import http
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AdminPasswordChangeForm, PasswordChangeForm
from ola.common.permissions import UserGroupManager, GROUP_NAME_MAP
from ola.common.utils import get_value_from_request
from models import Subscriber
from forms import SubscriberCreationForm
from client.forms import ClientForm
from ajax import SubscriberAjaxHandler, SubscriberNotificationAjaxHandler
from django.views.generic import View
from constants import *

# Create your views here.
class SubscriberAPI(View):
	def get(self, request):
		request_values = {}
		for key, value in request.GET.iteritems():
			request_values.update({key: value})
		ajaxMainClass = SubscriberAjaxHandler()
		ajaxMainClass.httpRequest = request
		ajaxMainClass.user = request.user
		funtionToCall = getattr(ajaxMainClass, request_values.pop('fn'), None)
		if not funtionToCall:
			return http.Http404

		responseValues = funtionToCall(**request_values)
		response = http.HttpResponse()
		response.status_code = 200
		response.write(responseValues)
		response['Content-Type'] = 'application/json'
		return response

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

class ApproverAPI(View):
	def get(self, request):
		ajaxMainClass = SubscriberAjaxHandler()
		ajaxMainClass.httpRequest = request
		ajaxMainClass.user = request.user
		funtionToCall = getattr(ajaxMainClass, 'get_approvers', None)
		if not funtionToCall:
			return http.Http404

		responseValues = funtionToCall(**request.GET.dict())
		response = http.HttpResponse()
		response.status_code = 200
		response.write(responseValues)
		response['Content-Type'] = 'application/json'
		return response	

class SubscriberRegistrationView(View):
	def get(self, request):
		context = {
			'user_creation_form' : UserCreationForm(),
			'subscriber_creation_form' : SubscriberCreationForm(),
			'client_form' : ClientForm()
		}
		return render(request, 'registration/registration.html', context)

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

class SubscriberCreateView(View):
	def get(self, request):
		auth_group = UserGroupManager.check_user_group(request.user)
		logged_in_employee = Subscriber.objects.get(user=request.user)
		context = {
			'auth_group' : auth_group,
			'subscriber_create_form' : SubscriberCreationForm(
				initial={
					'role' : Group.objects.get(name__exact=GROUP_NAME_MAP['LEAVE_APPROVER']).id
				}
			),
			'user_creation_form' : UserCreationForm(),
			'logged_in_employee' : logged_in_employee,
		}
		return render(request, 'subscriber/account_create.html', context)

class SubscriberView(View):
	def get(self, request):
		auth_group = UserGroupManager.check_user_group(request.user)
		if not UserGroupManager.is_company_admin(request.user):
			return http.HttpResponseRedirect(reverse('home_page'))

		logged_in_employee = Subscriber.objects.get(user=request.user)
		context = {
			'auth_group' : auth_group,
			'logged_in_employee' : logged_in_employee,
		}
		return render(request, 'subscriber/subscribers.html', context)

class SubscriberDetailsFormView(View):
	def get(self, request, user_id):
		auth_group = UserGroupManager.check_user_group(request.user)
		user = User.objects.get(pk=int(user_id))
		subscriber = Subscriber.objects.get(user__id__exact=int(user_id))
		logged_in_employee = Subscriber.objects.get(user=request.user)
		if logged_in_employee.id != subscriber.id:
			if not UserGroupManager.is_company_admin(request.user):
				return http.HttpResponseRedirect(reverse('home_page'))

		password_change_form = PasswordChangeForm(user=request.user)
		if UserGroupManager.is_company_admin(request.user):
			password_change_form = AdminPasswordChangeForm(user=user)
		context = {
			'auth_group' : auth_group,
			'password_change_form' : password_change_form,
			'subscriber_change_form' : SubscriberCreationForm(),
			'user_change_form' : UserChangeForm(instance=subscriber.user),
			'logged_in_employee' : logged_in_employee,
			'user' : user,
			'subscriber' : subscriber,
			'user_id' : user_id
		}
		return render(request, 'subscriber/account_settings.html', context)

class SubscriberDetailsAPI(View):
	def get(self, request, user_id):
		ajaxMainClass = SubscriberAjaxHandler()
		ajaxMainClass.httpRequest = request
		ajaxMainClass.user = request.user
		funtionToCall = getattr(ajaxMainClass, 'get_user', None)
		if not funtionToCall:
			return http.Http404

		responseValues = funtionToCall(user_id)
		response = http.HttpResponse()
		response.status_code = 200
		response.write(responseValues)
		response['Content-Type'] = 'application/json'
		return response

	def post(self, request, user_id):
		args = json.loads(request.body)
		ajaxMainClass = SubscriberAjaxHandler()
		ajaxMainClass.httpRequest = request
		ajaxMainClass.user = request.user
		funtionToCall = getattr(ajaxMainClass, args.pop(), None)
		if not funtionToCall:
			return http.Http404

		args.append(user_id)
		responseValues = funtionToCall(*args)
		response = http.HttpResponse()
		response.status_code = 200
		response.write(responseValues)
		response['Content-Type'] = 'application/json'
		return response

class SubscriberNotificationAPI(View):
	def get(self, request, user_id):
		request_values = {}
		for key, value in request.GET.iteritems():
			request_values.update({key: value})
		ajaxMainClass = SubscriberNotificationAjaxHandler()
		ajaxMainClass.httpRequest = request
		ajaxMainClass.user = request.user
		funtionToCall = getattr(ajaxMainClass, request_values.pop('fn'), 'get_all')
		if not funtionToCall:
			return http.Http404

		responseValues = funtionToCall(user_id, **request_values)
		response = http.HttpResponse()
		response.status_code = 200
		response.write(responseValues)
		response['Content-Type'] = 'application/json'
		return response

	def post(self, request, user_id):
		args = json.loads(request.body)
		ajaxMainClass = SubscriberNotificationAjaxHandler()
		ajaxMainClass.httpRequest = request
		ajaxMainClass.user = request.user
		funtionToCall = getattr(ajaxMainClass, args.pop(), None)
		if not funtionToCall:
			return http.Http404

		args.append(user_id)
		responseValues = funtionToCall(*args)
		response = http.HttpResponse()
		response.status_code = 200
		response.write(responseValues)
		response['Content-Type'] = 'application/json'
		return response