from django.db import models

class HRecipe(models.Model):
    """ Representation of an hrecipe-based recipe (see http://microformats.org/wiki/hrecipe) """
    name = models.CharField(max_length=40) # hrecipe field name is "fn"
#    ingredient (1 or more)
#        value/type
    yields = models.CharField(max_length=40) # optional
    instructions = models.TextField()
    duration = models.CharField(max_length=40) # 1 or more, optional
#    photo
    summary = models.CharField(max_length=80) # optional
    author = models.CharField(max_length=30) # 1 or more, optional
    published = models.DateField() # optional
#    nutrition (1 or more)
#        value/type
    tag = models.CharField(max_length=15)# optional, 1 or more

    def __unicode__(self):
        return self.name

class Recipe(HRecipe):
    """ A recipe object """
    submitter = models.CharField(max_length=20)
    def __unicode__(self):
        return self.name + ", submitted by " + self.submitter

