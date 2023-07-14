from django.shortcuts import render
from django_pandas.io import read_frame
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Players, Tournaments, Strokesgained, Rounds
from .serializers import PlayersSerializer, TournamentsSerializer, StrokesgainedSerializer, RoundsSerializer
from collections import OrderedDict

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

@api_view(['GET'])
def get_tournaments(request):
    '''A view to return a list of all tournaments in the database'''
    data = Tournaments.objects.all()
    serializer = TournamentsSerializer(data, many=True)

    return Response(serializer.data)

@api_view(['GET'])
def get_strokesgained(request):
    '''A view to return a list of all strokesgained in the database'''
    data = Strokesgained.objects.all()
    serializer = StrokesgainedSerializer(data, many=True)

    return Response(serializer.data)

@api_view(['GET'])
def get_rounds(request):
    '''A view to return a list of all rounds in the database'''
    data = Rounds.objects.all()
    serializer = RoundsSerializer(data, many=True)

    return Response(serializer.data)

@api_view(['GET'])
def get_players_detail(request, name):
    '''A view to return a list from a query in the database'''
    try:
        data = Players.objects.filter(name__icontains=name)
        serializer = PlayersSerializer(data, many=True)
        return Response(serializer.data)
    
    except Players.DoesNotExist:
        return Response("Player not found")
    
@api_view(['GET'])
def get_tournaments_detail(request, name=None):
    '''A view to return tournament stats by player'''
    if name:
        try:
            # get player name from Players table
            player = Players.objects.filter(name__icontains=name).values('player_id')
            stats = Strokesgained.objects.filter(player__in=player)
            serializer = StrokesgainedSerializer(stats, many=True)

            cols = ['id', 'tournament', 'round', 'name', 'total', 'round_score', 'sg_putt', 'sg_arg', 'sg_app', 'sg_ott', 'sg_t2g', 'sg_total']
            for i in serializer.data:
                player_id: int = i['player']
                name = Players.objects.filter(player_id=player_id).values('name')
                i['name'] = name[0]['name']

            new_data = []
            for i in serializer.data:
                new_data.append(OrderedDict((k, i[k]) for k in cols))

            return Response(new_data)
    
        except Players.DoesNotExist:
            return Response("Player not found")
        
    else:
        # get player name from Players table
        player = Players.objects.all().values('player_id')
        stats = Strokesgained.objects.all()
        serializer = StrokesgainedSerializer(stats, many=True)

        cols = ['id', 'tournament', 'round', 'name', 'total', 'round_score', 'sg_putt', 'sg_arg', 'sg_app', 'sg_ott', 'sg_t2g', 'sg_total']
        for i in serializer.data:
            player_id: int = i['player']
            name = Players.objects.filter(player_id=player_id).values('name')
            i['name'] = name[0]['name']

        new_data = []
        for i in serializer.data:
            new_data.append(OrderedDict((k, i[k]) for k in cols))

        return Response(new_data)