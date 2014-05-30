from django import forms
from models import Leave
from ola.common.forms import StrippedCharField

class LeaveForm(forms.ModelForm):
	leave_type = forms.ChoiceField(widget=forms.Select(attrs={'class':'form-control', 'ng-model':'leave.type', 'ng-required':'true'}), required=True)
	approvers = StrippedCharField(widget=forms.TextInput(attrs={'placeholder':'Send Request To', 'class':'form-control', 'ng-model':'leave.approver', 'ng-required':'true'}), required=True)
	class Meta:
		model = Leave
		exclude = ['type_of_leave', 'requester', 'approver', 'status', 'created_on']