from tomcookery.app.models import *
from django.contrib import admin

class CookoffThemeAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

class RecipeAdmin(admin.ModelAdmin):
    prepopulated_fields = {'url': ('name',)}

admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredient)
admin.site.register(Duration)
admin.site.register(Photo)
admin.site.register(Tag)
admin.site.register(ChefRank)
admin.site.register(MyProfile)
admin.site.register(Ingredient_Measurement)
admin.site.register(CookoffTheme, CookoffThemeAdmin)