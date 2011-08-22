from tomcookery.app.models import *

def votingOpen():
	if CookoffTheme.objects.currentTheme():
		return CookoffTheme.objects.currentTheme().voteOpen()
	else:
		return False

def submitOpen():
	if CookoffTheme.objects.currentTheme():
		return CookoffTheme.objects.currentTheme().submissionsOpen()
	else:
		return False

def votingContext(request):
	'Adds our current theme status to the request context'
	return {'currentTheme':CookoffTheme.objects.currentTheme(),
		'votingOpen': votingOpen(),
		'submissionsOpen': submitOpen(), 
	}