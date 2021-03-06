import json
import datetime
from django import http
from django.shortcuts import render
from django.core.urlresolvers import reverse
from ola.common.permissions import UserGroupManager
from forms import LeaveForm, LeaveTypeForm
from django.views.generic import View
from ajax import LeaveAjaxHandler, LeaveTypeAjaxHandler, HolidayAjaxHandler
# Create your views here.
class LeaveAPI(View):
	def get(self, request):
		ajaxMainClass = LeaveAjaxHandler()
		ajaxMainClass.httpRequest = request
		ajaxMainClass.user = request.user
		funtionToCall = getattr(ajaxMainClass, request.GET.get('fn'), None)
		if not funtionToCall:
			return http.Http404

		responseValues = funtionToCall()
		response = http.HttpResponse()
		response.status_code = 200
		response.write(responseValues)
		response['Content-Type'] = 'application/json'
		return response

	def post(self, request):
		args = json.loads(request.body)
		ajaxMainClass = LeaveAjaxHandler()
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

class LeaveTypeAPI(View):
	def get(self, request):
		ajaxMainClass = LeaveTypeAjaxHandler()
		ajaxMainClass.httpRequest = request
		ajaxMainClass.user = request.user
		funtionToCall = getattr(ajaxMainClass, request.GET.get('fn'), None)
		if not funtionToCall:
			return http.Http404

		responseValues = funtionToCall()
		response = http.HttpResponse()
		response.status_code = 200
		response.write(responseValues)
		response['Content-Type'] = 'application/json'
		return response

	def post(self, request):
		args = json.loads(request.body)
		ajaxMainClass = LeaveTypeAjaxHandler()
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

class LeaveTypeFormView(View):
	def get(self, request):
		auth_group = UserGroupManager.check_user_group(request.user)
		if not UserGroupManager.is_company_admin(request.user):
			raise UnauthorizedException('Access Violation')
		context = {
			'auth_group' : auth_group,
			'leave_type_form' : LeaveTypeForm()
		}
		return render(request, 'leave/leave_type_form.html', context)

class SubscriberLeaveAPI(View):
	def get(self, request, user_id):
		ajaxMainClass = LeaveAjaxHandler()
		ajaxMainClass.httpRequest = request
		ajaxMainClass.user = request.user
		funtionToCall = getattr(ajaxMainClass, 'get_subscriber_leave_requests', None)
		if not funtionToCall:
			return http.Http404

		responseValues = funtionToCall(user_id, **request.GET.dict())
		response = http.HttpResponse()
		response.status_code = 200
		response.write(responseValues)
		response['Content-Type'] = 'application/json'
		return response

class HolidayAPI(View):
	def get(self, request):
		start_date = request.GET.get('fd')
		end_date = request.GET.get('td')
		ajaxMainClass = HolidayAjaxHandler()
		ajaxMainClass.httpRequest = request
		ajaxMainClass.user = request.user
		funtionToCall = getattr(ajaxMainClass, request.GET.get('fn'), None)
		if not funtionToCall:
			return http.Http404

		responseValues = funtionToCall(start_date, end_date)
		response = http.HttpResponse()
		response.status_code = 200
		response.write(responseValues)
		response['Content-Type'] = 'application/json'
		return response

	def post(self, request):
		args = json.loads(request.body)
		ajaxMainClass = HolidayAjaxHandler()
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

class ApproverLeaveAPI(View):
	def get(self, request, user_id):
		ajaxMainClass = LeaveAjaxHandler()
		ajaxMainClass.httpRequest = request
		ajaxMainClass.user = request.user
		funtionToCall = getattr(ajaxMainClass, 'get_pending_approvals_for_subscriber', None)
		if not funtionToCall:
			return http.Http404

		responseValues = funtionToCall(user_id, **request.GET.dict())
		response = http.HttpResponse()
		response.status_code = 200
		response.write(responseValues)
		response['Content-Type'] = 'application/json'
		return response	

class HolidayFormView(View):
	def get(self, request):
		auth_group = UserGroupManager.check_user_group(request.user)
		if not UserGroupManager.is_company_admin(request.user):
			raise UnauthorizedException('Access Violation')
		context = {
			'auth_group' : auth_group
		}
		return render(request, 'leave/holidays.html', context)

class LeaveApproveView(View):
	def get(self, request):
		auth_group = UserGroupManager.check_user_group(request.user)
		if not UserGroupManager.is_company_admin(request.user):
			if not UserGroupManager.can_approve_leave(request.user):
				return http.HttpResponseRedirect(reverse('home_page'))
		context = {
			'auth_group' : auth_group
		}
		return render(request, 'leave/pending_approval.html', context)
