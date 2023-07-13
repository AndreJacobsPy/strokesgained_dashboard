from django.shortcuts import render
from django_pandas.io import read_frame
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Players, Tournaments, Strokesgained, Rounds
from .serializers import PlayersSerializer, TournamentsSerializer, StrokesgainedSerializer, RoundsSerializer


# Create your views here.
def players_list(request):
    '''A view to return a list of all players in the database'''
    data = Players.objects.all()
    df = read_frame(data).set_index('player_id')

    return render(request, 'players.html', {'df': df.to_html()})

def courses_list(request):
    '''A view to return a list of all courses in the database'''
    data = Tournaments.objects.all()
    df = read_frame(data).set_index('tournament_id')

    return render(request, 'courses.html', {'df': df.to_html()})

@api_view(['GET'])
def get_players(request):
    '''A view to return a list of all players in the database'''
    data = Players.objects.all()
    serializer = PlayersSerializer(data, many=True)

    return Response(serializer.data)