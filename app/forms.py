from django import forms

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

class ProfileForm(forms.Form):
    first_name = forms.CharField(max_length = 30, label = 'First Name')
    last_name = forms.CharField(max_length = 30, label = 'Last Name')
    #(Optional) Make email unique.
    email = forms.EmailField(label = 'Email Address')
