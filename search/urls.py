from django.urls import include, path

from . import views

api_patterns = [
    path('search/', views.search, name='api_search'),
    path('person-search/', views.person_search, name='api_person_search'),
]

urlpatterns = [
    path('', views.index, name='index'),
    path('profile/', views.profile, name='profile'),
    path('api/', include(api_patterns))
]
