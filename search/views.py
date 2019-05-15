from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render

from search.models import Category
from .models import Person, Project


def index(request):
    categories = Category.objects.filter()

    context = {
        'categories': categories
    }
    return render(request, 'search/index.html', context)


def profile(request):
    return render(request, 'search/profile.html', {})


def search(request):
    search_query = request.GET.get('q', '')
    if search_query:
        search_query = search_query.strip()

    location = request.GET.get('location', '')
    if location:
        location = location.strip()

    category_id = request.GET.get('category', '')
    category = None
    if category_id:
        category = Category.objects.filter(pk=category_id).first()

    # get user name like search query
    persons = Person.objects.filter(name__icontains=search_query)
    if location:
        persons = persons.filter(location__icontains=location)

    # get project name like search query
    projects = Project.objects.filter(
        Q(name__icontains=search_query) |
        Q(creator__name__icontains=search_query)
    )
    if location:
        projects = projects.filter(location__icontains=location)
    if category:
        projects = projects.filter(category=category)

    return JsonResponse({
        'projects': list(
            map(lambda p: {
                'name': p.name,
                'creator': p.creator.name,
                'location': p.location,
                'category': p.category.name,
                'short_description': p.short_description
            }, projects)),
        'persons': list(map(lambda p: p.name, persons)),
    })
