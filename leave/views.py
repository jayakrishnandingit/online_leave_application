import json
from django import http
from django.shortcuts import render
from ola.common.permissions import UserGroupManager
from forms import LeaveForm, LeaveTypeForm
from django.views.generic import View
from ajax import LeaveTypeAjaxHandler
# Create your views here.
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

class HolidayFormView(View):
	def get(self, request):
		auth_group = UserGroupManager.check_user_group(request.user)
		if not UserGroupManager.is_company_admin(request.user):
			raise UnauthorizedException('Access Violation')
		context = {
			'auth_group' : auth_group
		}
		return render(request, 'leave/holidays.html', context)