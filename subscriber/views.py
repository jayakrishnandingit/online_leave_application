import json
from django import http
from django.shortcuts import render
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AdminPasswordChangeForm, PasswordChangeForm
from ola.common.permissions import UserGroupManager, GROUP_NAME_MAP
from ola.common.utils import get_value_from_request
from models import Subscriber
from forms import SubscriberCreationForm
from client.forms import ClientForm
from subscriber.ajax import SubscriberAjaxHandler
from django.views.generic import View
from constants import *

# Create your views here.
def register(request):
	context = {
		'user_creation_form' : UserCreationForm(),
		'subscriber_creation_form' : SubscriberCreationForm(),
		'client_form' : ClientForm()
	}
	return render(request, 'registration/registration.html', context)

class SubscriberAPI(View):
	def get(self, request):
		page_no = int(request.GET.get('page_no', 1))
		no_of_records = int(request.GET.get('no_of_records', NUMBER_OF_VALUES_PER_PAGE))
		show_all = bool(int(request.GET.get('show_all', 0)))

		ajaxMainClass = SubscriberAjaxHandler()
		ajaxMainClass.httpRequest = request
		ajaxMainClass.user = request.user
		funtionToCall = getattr(ajaxMainClass, request.GET.get('fn'), None)
		if not funtionToCall:
			return http.Http404

		responseValues = funtionToCall(page_no, no_of_records, show_all)
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
			raise UnauthorizedException('Access Violation')

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
				# make this exception redirect user to home page
				raise UnauthorizedException('Access Violation')
		password_change_form = PasswordChangeForm(user=request.user)
		if UserGroupManager.is_company_admin(request.user):
			password_change_form = AdminPasswordChangeForm(user=user)
		context = {
			'auth_group' : auth_group,
			'password_change_form' : password_change_form,
			'subscriber_change_form' : SubscriberCreationForm(),
			'user_change_form' : UserChangeForm(),
			'logged_in_employee' : logged_in_employee,
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
