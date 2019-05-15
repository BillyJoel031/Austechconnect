from django.urls import include, path

from . import views

api_patterns = [
    path('search/', views.search, name='api_search')
]

urlpatterns = [
    path('', views.index, name='index'),
    path('profile/', views.profile, name='profile'),
    path('api/', include(api_patterns))
]
