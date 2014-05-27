from django import forms
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
