from tomcookery.app.models import *
from django.contrib import admin

admin.site.register(Recipe)
admin.site.register(Ingredient)
admin.site.register(Duration)
admin.site.register(Photo)
admin.site.register(Tag)
admin.site.register(Ingredient_Measurement)