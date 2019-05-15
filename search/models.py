from django.db import models


class Person(models.Model):
    id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=40, help_text='First Name', blank=False, null=False)
    location = models.CharField(max_length=30, help_text='Location', blank=True)
    joined_date = models.DateTimeField(auto_now=True)
    about = models.TextField(blank=True, null=True)

    def get_name(self):
        return '{} - {}'.format(self.name, self.location)

    def __str__(self):
        return self.get_name()


class Category(models.Model):
    name = models.CharField(max_length=20, help_text='Category name', blank=False, null=False)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return '{}'.format(self.name)


class Project(models.Model):
    id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=255, help_text='Project name', blank=False, null=False)
    short_description = models.TextField(help_text='Short description')
    location = models.CharField(max_length=30, help_text='Location', blank=True)
    category = models.ForeignKey(Category, help_text='Project category', on_delete=models.SET_NULL,
                                 blank=True, null=True)
    creator = models.ForeignKey(Person, on_delete=models.CASCADE)

    def __str__(self):
        return '{} - {}'.format(self.name, self.category.name)
