from django.urls import path
from . import views

urlpatterns = [
    path('players-view/', views.players_list),
    path('courses-view/', views.courses_list),
    path('players-api/', views.get_players),
    path('tournaments-api/', views.get_tournaments),
    path('strokesgained-api/', views.get_strokesgained),
    path('rounds-api/', views.get_rounds),
    path('players-detail-api/<str:name>/', views.get_players_detail),
    path('tournaments-detail-api/<str:name>/', views.get_tournaments_detail),
]