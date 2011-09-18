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
	returnedcontext= {
		'currentTheme':CookoffTheme.objects.currentTheme(),
		'recentlyClosedTheme':CookoffTheme.objects.recentlyClosedTheme(),
		'votingOpen': votingOpen(),
		'submissionsOpen': submitOpen(), 
	}
	if request.user and CookoffTheme.objects.currentTheme():
		"if there is a user and current theme find out what the user has voted for."
		try:	
			userVote = {
			'userIngVoteOpen':request.user.get_profile().userVotedThemeIng(CookoffTheme.objects.currentTheme()),
			'useroverallVoteOpen':request.user.get_profile().userVotedThemeOverall(CookoffTheme.objects.currentTheme()),
			#usercustomVoteOpen:request.user.get_profile().,
			}
			userVote['userThemeVoteOpen']=request.user.get_profile().userVotedThemeTheme(CookoffTheme.objects.currentTheme())
		except:
			userVote = {
			'userIngVoteOpen':False,
			'useroverallVoteOpen':False,
			#usercustomVoteOpen:request.user.get_profile().,
			}
			userVote['userThemeVoteOpen']= False
		returnedcontext.update(userVote)
	return returnedcontext