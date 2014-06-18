from django import forms
from django.core.exceptions import ValidationError
from models import Leave, LeaveType, Holiday
from subscriber.models import Subscriber
from ola.common.forms import StrippedCharField
from ola.settings import DATE_INPUT_FORMATS, DATETIME_INPUT_FORMATS
from ola.common.permissions import GROUP_NAME_MAP

class LeaveTypeForm(forms.ModelForm):
	class Meta:
		model = LeaveType
		exclude= ['client', 'created_on', 'created_by']

class HolidayForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super(HolidayForm, self).__init__(*args, **kwargs)
		self.fields['start'].input_formats = [DATE_INPUT_FORMATS[0]]
		self.fields['end'].input_formats = [DATE_INPUT_FORMATS[0]]

	class Meta:
		model = Holiday
		exclude = ['client', 'created_on', 'created_by']

class LeaveForm(forms.ModelForm):
	def __init__(self, logged_in_employee, *args, **kwargs):
		super(LeaveForm, self).__init__(*args, **kwargs)
		self.fields['leave_type'].choices = [(str(ltyp.id), str(ltyp.type_of_leave)) for ltyp in LeaveType.objects.filter(client=logged_in_employee.client)]
		approvers = Subscriber.objects.filter(
			client=logged_in_employee.client,
			user__groups__name__in=[GROUP_NAME_MAP['LEAVE_APPROVER'], GROUP_NAME_MAP['COMPANY_ADMIN']]
		).exclude(
			id__exact=logged_in_employee.id
		)
		self.fields['approver'].choices = [(str(app.user.id), str(app.name)) for app in approvers]
		self.fields['start'].input_formats = [DATETIME_INPUT_FORMATS[1]]
		self.fields['end'].input_formats = [DATETIME_INPUT_FORMATS[1]]

	leave_type = forms.ChoiceField(choices=[], widget=forms.Select(attrs={'class':'form-control', 'ng-model':'form_data.leave_type', 'ng-required':'true'}), required=True)
	approver = forms.ChoiceField(choices=[], widget=forms.Select(), required=True)

	class Meta:
		model = Leave
		exclude = ['type_of_leave', 'requester', 'approver', 'status', 'created_on']