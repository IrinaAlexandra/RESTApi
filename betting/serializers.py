from rest_framework import serializers
from .models import Sport, Event, Market, Selection

class SportSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=True)

    class Meta:
        model = Sport
        fields = ('id', 'name')
        depth = 1

class SelectionSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    class Meta:
        model = Selection
        exclude = ('market','event')

class MarketSerializer(serializers.ModelSerializer):
    selections = SelectionSerializer(many=True)
    id = serializers.IntegerField()
    class Meta:
        model = Market
        fields = ['id', 'name', 'selections']


class EventSerializer(serializers.ModelSerializer):   
    markets = MarketSerializer(many=True)    
    sport = SportSerializer()
    id = serializers.IntegerField(required=True) 
    
    class Meta:
        model = Event
        fields = ['id','url', 'name', 'start_time', 'sport', 'markets']
        depth = 1
    
    def create(self, validated_data):
        selections = []
        sport_data = validated_data.pop('sport', None)
        if sport_data:
            sport = Sport.objects.create(**sport_data)
        market_data = validated_data.pop('markets', None)[0]
        if market_data:
            selections =market_data.pop('selections', None)
            market = Market.objects.create(sport=sport, **market_data)
        event = Event.objects.create(sport=sport, **validated_data)
        for selection in selections:
            Selection.objects.create(event=event, market=market, **selection)
        return event


class EventSerializerFilter(serializers.ModelSerializer):

    class Meta:
        model = Event
        fields = ['id', 'url', 'name', 'start_time']

