from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import Group, User
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
	role = forms.ChoiceField(
		choices=[('', '----Select Role----')] + [(str(grp.id), str(grp.name)) for grp in Group.objects.all()],
		widget=forms.Select(
			attrs={
				'class' : 'form-control',
				'ng-model' : 'form_data.role',
				'ng-required' : 'true',
				'ng-selected' : 'subscriber.group.id',
			}
		),
		required=False
	)
	hidden_user = StrippedCharField(
		widget=forms.HiddenInput(
			attrs={
				'ng-model' : 'form_data.id'
			}
		),
		required=False
	)
	is_company_admin = False
	logged_in_employee = None
	user_changed = None
	auth_group = None

	def clean_role(self):
		if self.is_company_admin:
			if not self.cleaned_data['role']:
				raise ValidationError('This field is required.')
		return self.cleaned_data['role']

	def clean_email(self):
		user_with_email = User.objects.filter(email__exact=self.cleaned_data['email']).first()
		if self.user_changed:
			if user_with_email and user_with_email.id != self.user_changed.id:
				raise ValidationError('User with email already exists.')
		elif user_with_email:
			raise ValidationError('User with email already exists.')
		return self.cleaned_data['email']