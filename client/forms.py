from django import forms
from models import Client

class ClientForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super(ClientForm, self).__init__(*args, **kwargs)

	class Meta:
		model = Client
		fields = ['name']