from django.shortcuts import render, redirect
from django.contrib import messages
from .templates.users.forms import UserRegisterForm

from search.models import Person
from random import randint

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            about = form.cleaned_data.get('about')
            profile = Person()
            profile.id = ''.join(["%s" % randint(0, 9) for num in range(0, 10)])
            profile.name = '{} {}'.format(first_name, last_name)
            profile.about = about
            profile.save()
            user.profile = profile
            user.save()

            print(user.profile)

            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


