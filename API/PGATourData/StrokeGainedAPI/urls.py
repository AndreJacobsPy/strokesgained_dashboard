from django.urls import path
from . import views

urlpatterns = [
    path('players-view/', views.players_list),
    path('courses-view/', views.courses_list),
    path('players-api/', views.get_players),
]