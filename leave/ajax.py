import copy
from ola.common.ajax import JSONParser
from ola.common.permissions import UserGroupManager, GROUP_NAME_MAP
from models import LeaveType
from forms import LeaveTypeForm
from subscriber.models import Subscriber
from django.contrib.auth.models import Group, User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger, InvalidPage

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
