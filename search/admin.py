from django.contrib import admin

from .models import Category, Person, PersonCategory, Project


class PersonAdmin(admin.ModelAdmin):
    search_fields = ('name', 'location', 'about')


class ProjectAdmin(admin.ModelAdmin):
    search_fields = ('name', 'location', 'short_description')


admin.site.register(Person, PersonAdmin)
admin.site.register(PersonCategory)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Category)
