from django import forms
class recipeNewSaveForm(forms.Form):
	name = forms.CharField(
		label=u'Name',
		widget=forms.TextInput(attrs={'size': 64})
	)
	ingredients = forms.CharField(
		label=u'Ingredient',
		widget=forms.HiddenInput()
	)
	yeilds = forms.CharField(
		label=u'Servings',
		widget=forms.TextInput(attrs={'size': 64})
	)
	instructions = forms.CharField(
		label=u'Instructions',
		widget=forms.Textarea()
	)
	durations = forms.IntegerField(
		label=u'Time to Cook',
		widget=forms.TextInput(attrs={'size': 4})
	)
	photos = forms.URLField(
		label=u'Image',
		widget=forms.FileInput(attrs={'size': 4})
	)
	authors = forms.CharField(
		label=u'Image',
		widget=forms.HiddenInput(attrs={'size': 4})
	)
	tags = forms.CharField(
		label=u'Tags',
		widget=forms.Textarea()
	)
