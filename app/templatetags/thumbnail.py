import os
import Image
from django.template import Library

register = Library()

def thumbnail(path, size='104x104'):

	#THIS NEEDS TO BE SWITCHED OUT!!!!!
    path = path.replace("http://localhost:8000","/Users/corygwin/django/tomcookery")
    # BAD!!!!!!!
    
    # defining the size
    x, y = [int(x) for x in size.split('x')]
    # defining the filename and the miniature filename
    filehead, filetail = os.path.split(path)
    basename, format = os.path.splitext(filetail)
    miniature = basename + '_' + size + format
    filename = path

    miniature_filename = os.path.join(filehead, miniature)
    filehead, filetail = os.path.split(path)
    miniature_url = filehead + '/' + miniature
    if os.path.exists(miniature_filename) and os.path.getmtime(filename)>os.path.getmtime(miniature_filename):
        os.unlink(miniature_filename)
    # if the image wasn't already resized, resize it
    if not os.path.exists(miniature_filename):
        image = Image.open(filename)
        image.thumbnail([x, y], Image.ANTIALIAS)
        try:
            image.save(miniature_filename, image.format, quality=90, optimize=1)
        except:
            image.save(miniature_filename, image.format, quality=90)
    #THIS NEEDS TO BE SWITCHED OUT!!!!!
	miniature_url = miniature_url.replace("/Users/corygwin/django/tomcookery","http://localhost:8000")
	# BAD!!!!!!!
	
    return miniature_url.replace("/Users/corygwin/django/tomcookery","http://localhost:8000")

register.filter(thumbnail)