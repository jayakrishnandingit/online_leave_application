from django import forms
from models import Leave, LeaveType, Holiday
from ola.common.forms import StrippedCharField
from ola.settings import DATE_INPUT_FORMATS

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

	leave_type = forms.ChoiceField(choices=[], widget=forms.Select(attrs={'class':'form-control', 'ng-model':'leave.type', 'ng-required':'true'}), required=True)
	approvers = StrippedCharField(widget=forms.TextInput(attrs={'placeholder':'Send Request To', 'class':'form-control', 'ng-model':'leave.approver', 'ng-required':'true'}), required=True)
	class Meta:
		model = Leave
		exclude = ['type_of_leave', 'requester', 'approver', 'status', 'created_on']