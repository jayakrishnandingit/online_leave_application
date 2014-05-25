from django import forms
from ola.common.forms import StrippedCharField
from models import Subscriber

class SubscriberCreationForm(forms.Form):
	first_name = StrippedCharField(widget = forms.TextInput(attrs = {'class' : 'form-control'}), required = True)
	last_name = StrippedCharField(widget = forms.TextInput(attrs = {'class' : 'form-control'}), required = True)
	email = forms.EmailField(widget = forms.TextInput(attrs = {'class' : 'form-control'}), required = True)
