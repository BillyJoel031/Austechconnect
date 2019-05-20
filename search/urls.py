from django.urls import include, path

from . import views
from .apps import SearchConfig

app_name = SearchConfig.name

api_patterns = [
    path('search/', views.search, name='api_search'),
    path('person-search/', views.person_search, name='api_person_search'),
]

urlpatterns = [
    path('', views.index, name='index'),
    path('profile/<int:person_id>', views.profile, name='profile'),
    path('api/', include(api_patterns))
]
