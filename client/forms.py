from django import forms
from ola.common.forms import StrippedCharField 
from models import Client

class ClientForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super(ClientForm, self).__init__(*args, **kwargs)

	name = StrippedCharField(widget = forms.TextInput(attrs = {'class' : 'form-control', 'ng-model' : 'form_data.name', 'ng-required' : 'true'}), required = True)

	class Meta:
		model = Client
		fields = ['name']