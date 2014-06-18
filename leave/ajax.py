import copy
import datetime
from ola.common.ajax import JSONParser
from ola.common.utils import get_month_end
from ola.common.permissions import UserGroupManager, GROUP_NAME_MAP
from models import LeaveType, Holiday
from forms import LeaveForm, LeaveTypeForm, HolidayForm
from subscriber.models import Subscriber
from django.contrib.auth.models import Group, User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger, InvalidPage
from ola.settings import DATE_INPUT_FORMATS
from mailer import SendNotification

class LeaveAjaxHandler(JSONParser):
	def request_leave(self, form_values):
		logged_in_employee = Subscriber.objects.get(user=self.user)
		form = LeaveForm(logged_in_employee, form_values)
		if form.is_valid():
			leave = form.save(commit=False)
			leave.type_of_leave = LeaveType.objects.get(pk=form.cleaned_data['leave_type'])
			leave.requester = logged_in_employee
			leave.approver = Subscriber.objects.get(user__id__exact=form.cleaned_data['approver'])
			leave.status = 0 # pending
			leave.save()
			SendNotification([leave.approver.user.email], leave.requester.user.email, 'leave_request', leave).start()
			return self.respond(is_saved=True)
		return self.respond(is_saved=False, errors=form.errors)

class LeaveTypeAjaxHandler(JSONParser):
	def get_all(self):
		logged_in_employee = Subscriber.objects.get(user=self.user)
		if not UserGroupManager.is_company_admin(self.user):
			raise UnauthorizedException('Access Violation')
		leave_types = LeaveType.objects.filter(client=logged_in_employee.client).order_by('created_on')
		serialized_objects = []
		for leave_type in leave_types:
			serialized_objects.append(leave_type.serialize())
		return self.respond(leave_types=serialized_objects)

	def save(self, form_values):
		logged_in_employee = Subscriber.objects.get(user=self.user)
		if not UserGroupManager.is_company_admin(self.user):
			raise UnauthorizedException('Access Violation')

		form = LeaveTypeForm(form_values, instance=LeaveType.objects.filter(pk=form_values.get('hidden_type_id')).first())
		if form.is_valid():
			leave_type = form.save(commit=False)
			leave_type.client = logged_in_employee.client
			leave_type.created_by = logged_in_employee
			leave_type.save()
			return self.respond(is_saved=True, leave_type=leave_type.serialize())
		return self.respond(is_saved=False)

	def delete(self, ids_to_delete):
		logged_in_employee = Subscriber.objects.get(user=self.user)
		if not UserGroupManager.is_company_admin(self.user):
			raise UnauthorizedException('Access Violation')
		LeaveType.objects.filter(id__in=ids_to_delete).delete()
		return self.respond(is_saved=True)

class HolidayAjaxHandler(JSONParser):
	def get_all(self, start, end):
		if not UserGroupManager.is_company_admin(self.user):
			raise UnauthorizedException('Access Violation')

		logged_in_employee = Subscriber.objects.get(user=self.user)
		if not start:
			start = datetime.datetime.today().replace(day=1).date()
		else:
			start = datetime.datetime.strptime(start, DATE_INPUT_FORMATS[0]).date()
		if not end:
			end = datetime.datetime.today().replace(day=get_month_end()).date()
		else:
			end = datetime.datetime.strptime(end, DATE_INPUT_FORMATS[0]).date()

		holidays = Holiday.objects.filter(
			client=logged_in_employee.client,
			start__gte=start,
			start__lte=end
		).order_by('start')
		serialized_objects = []
		for holiday in holidays:
			serialized_objects.append(holiday.serialize())
		return self.respond(holidays=serialized_objects)

	def save(self, form_values):
		if not UserGroupManager.is_company_admin(self.user):
			raise UnauthorizedException('Access Violation')
		logged_in_employee = Subscriber.objects.get(user=self.user)

		form = HolidayForm(form_values, instance=Holiday.objects.filter(pk=form_values.get('id')).first())
		if form.is_valid():
			holiday = form.save(commit=False)
			holiday.client = logged_in_employee.client
			holiday.created_by = logged_in_employee
			holiday.save()
			return self.respond(is_saved=True, holiday=holiday.serialize())
		return self.respond(is_saved=False, errors=form.errors)

	def delete(self, holiday_id):
		if not UserGroupManager.is_company_admin(self.user):
			raise UnauthorizedException('Access Violation')
		logged_in_employee = Subscriber.objects.get(user=self.user)

		Holiday.objects.get(pk=holiday_id).delete()
		return self.respond(is_saved=True)