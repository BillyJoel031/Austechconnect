from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from search.models import Category, PersonCategory
from search.utils import person_2_dict
from .models import Person, Project


def about(request):
    return HttpResponse('<h1>Home Page</h1>')


def index(request):
    categories = Category.objects.filter()
    person_categories = PersonCategory.objects.filter()

    context = {
        'categories': categories,
        'person_categories': person_categories,
    }
    return render(request, 'search/index.html', context)


def profile(request, person_id):
    person = get_object_or_404(Person, pk=person_id)
    context = {
        'person': person
    }
    return render(request, 'search/profile.html', context)


def person_search(request):
    search_query = request.GET.get('q', '')
    if search_query:
        search_query = search_query.strip()

    location = request.GET.get('location', '')
    if location:
        location = location.strip()

    category_id = request.GET.get('category', '')
    category = None
    if category_id:
        category = PersonCategory.objects.filter(pk=category_id).first()

    # remove redundant whitespaces
    search_query = ' '.join(search_query.split())

    # keywords search
    words = search_query.split(' ')
    condition = Q(name__icontains=search_query) | Q(about__icontains=search_query)
    for word in words:
        condition |= Q(about__icontains=word)
    persons = Person.objects.filter(condition)

    # keep filtering by location
    if location:
        persons = persons.filter(location__icontains=location)

    # keep filtering by categories
    if category:
        subcategories = PersonCategory.objects.filter(parent=category)
        condition = Q(category=category)
        if subcategories:
            '''This categories has sub-categories => extends the filter on sub-categories'''
            for c in subcategories:
                condition |= Q(category=c)
        persons = persons.filter(condition)

    persons = list(map(lambda p: person_2_dict(p), persons))
    return JsonResponse({
        'persons': persons
    })


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
