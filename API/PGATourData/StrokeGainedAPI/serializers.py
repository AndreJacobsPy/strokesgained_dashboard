from rest_framework import serializers
from .models import Players, Tournaments, Strokesgained, Rounds

class PlayersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Players
        fields = '__all__'

class TournamentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tournaments
        fields = '__all__'

class StrokesgainedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Strokesgained
        fields = '__all__'

class RoundsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rounds
        fields = '__all__'