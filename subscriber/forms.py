from django import forms
from django.contrib.auth.models import Group
from ola.common.forms import StrippedCharField
from models import Subscriber

class SubscriberCreationForm(forms.Form):
	first_name = StrippedCharField(
		widget = forms.TextInput(
			attrs = {
				'class' : 'form-control', 
				'ng-model':'form_data.first_name', 
				'ng-required' : 'true'
			}
		), 
		required = True
	)
	last_name = StrippedCharField(
		widget = forms.TextInput(
			attrs = {
				'class' : 'form-control', 
				'ng-model':'form_data.last_name', 
				'ng-required' : 'true'
			}
		), 
		required = True
	)
	email = forms.EmailField(
		widget = forms.EmailInput(
			attrs = {
				'class' : 'form-control', 
				'ng-model':'form_data.email', 
				'ng-required' : 'true'
			}
		), 
		required = True
	)
	no_of_leave_remaining = forms.IntegerField(
		widget=forms.TextInput(
			attrs={
				'class' : 'form-control', 
				'ng-model':'form_data.no_of_leave_remaining', 
				'ng-required' : 'false'	
			}
		),
		required=False
	)
	role = forms.ChoiceField(
		choices=[('', '')] + [(str(grp.id), str(grp.name)) for grp in Group.objects.all()],
		widget=forms.Select(
			attrs={
				'class' : 'form-control',
				'ng-model' : 'form_data.role',
				'ng-required' : 'true'
			}
		),
		required=True
	)
	need_to_check_leave = False
	logged_in_employee = None
	user_changed = None
	auth_group = None

	def clean_no_of_leave_remaining(self):
		if need_to_check_leave:
			if self.logged_in_employee.user.id != self.user_changed.id:
				if not self.cleaned_data['no_of_leave_remaining'] and self.cleaned_data['no_of_leave_remaining'] != 0:
					raise ValidationError('This field is required.')
			if self.cleaned_data['no_of_leave_remaining'] < 0:
				raise ValidationError('Invalid Entry')
		return self.cleaned_data['no_of_leave_remaining']

