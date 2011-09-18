from celery.task.schedules import crontab
from celery.decorators import periodic_task
from tomcookery.app.models import *

# see http://celeryproject.org/docs/reference/celery.task.schedules.html#celery.task.schedules.crontab
@periodic_task(run_every=crontab(hour="23", minute="57", day_of_week="*"))
def checkStatusTheme():
	"Checks the current theme at 11:53 every night to see if it is closed. If so results are tallied."    
	print "firing test task" 
	CookoffTheme.objects.closeTheme()
    