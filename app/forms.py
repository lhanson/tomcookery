from django import forms
import re
from django.contrib.auth.models import User

class recipeNewSaveForm(forms.Form):
	name = forms.CharField(
	label=u'Name',
	widget=forms.TextInput(attrs={'size': 64})
	)
	ingredients = forms.CharField(
	required=True,
	widget=forms.HiddenInput()
	)
	summary = forms.CharField(
	widget=forms.Textarea()
	)
	
	instructions = forms.CharField(
	label=u'Instructions',
	widget=forms.Textarea()
	)
	
	photo=forms.ImageField(required=False)
	
	yields = forms.CharField(
	label=u'Number of servings?',
	required=False,
	widget=forms.TextInput(attrs={'size': 4})
	)
	
	durations = forms.CharField(
	required=False,
	widget=forms.TextInput(attrs={'size':4})
	)
	
	tags = forms.CharField(
	label=u'Tags',
	widget=forms.TextInput(attrs={'size': 64, "placeholder":"e.g. thai, curry, easy"})
	)

class RegistrationForm(forms.Form):
	username = forms.CharField(label=u"Username", max_length=30)
	email= forms.EmailField(label=u"Email")
	password1 = forms.CharField(
		label=u"Password",
		widget=forms.PasswordInput()
		)
	password2 = forms.CharField(
		label=u"Password (Again)",
		widget=forms.PasswordInput()
		)
	def clean_password2(self):
		if 'password1' in self.cleaned_data:
			password1 = self.cleaned_data['password1']
			password2 = self.cleaned_data['password2']
			if password1 == password2:
				return password2
			else:
				raise forms.ValidationError('Passwords do not match. %s' % [password1])
		
	def clean_username(self):
		username = self.cleaned_data['username']
		if not re.search(r'^\w+$', username):
			raise forms.ValidationError('Username can only contain alphanumeric characters and the underscore.')
		try:
			User.objects.get(username = username)
		except User.DoesNotExist:
			return username
		raise forms.ValidationError('Username already in use')

class ProfileForm(forms.Form):
    first_name = forms.CharField(max_length = 30, label = 'First Name')
    last_name = forms.CharField(max_length = 30, label = 'Last Name')
    #(Optional) Make email unique.
    email = forms.EmailField(label = 'Email Address')
