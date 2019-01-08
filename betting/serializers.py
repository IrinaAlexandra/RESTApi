from rest_framework import serializers
from .models import Sport, Event, Market, Selection
from rest_framework.fields import empty

class SportSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=True) #required when creating a new instance
    class Meta:
        model = Sport
        fields = ('id', 'name')
        depth = 1

class SelectionSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=True)
    class Meta:
        model = Selection
        exclude = ('market','event') # will not show these ids when displaying event data as shown in implementation details

class MarketSerializer(serializers.ModelSerializer):
    selections = SelectionSerializer(many=True)
    id = serializers.IntegerField()
    class Meta:
        model = Market
        fields = ['id', 'name', 'selections']
        depth = 1

class EventSerializer(serializers.ModelSerializer):
    sport = SportSerializer()
    id = serializers.IntegerField(required=True) 
    markets = MarketSerializer(many=True)
    
    class Meta:
        model = Event
        fields = ['id','url', 'name', 'start_time', 'sport', 'markets']
        depth = 1
    
    def create(self, validated_data):
        """
        Function that takes all the data in the NewEvent and creates the event(match),
        sport (if sport id doesn't allready exists), market(same, checks if market already exists, if it does, it will
        use that) and the selections
        """
        selections = []
        sport_data = validated_data.pop('sport', None)
        if sport_data:
            sport_id = sport_data.get('id')
            if Sport.objects.filter(id =sport_id).exists():
                sport = Sport.objects.get(pk=sport_id)
            else:
                sport = Sport.objects.create(**sport_data)
        market_data = validated_data.pop('markets', None)[0]
        if market_data:
            selections =market_data.pop('selections', None)
            market_id = market_data.get('id')
            if Market.objects.filter(id =market_id).exists():
                market = Market.objects.get(pk=market_id)
            else:
                market = Market.objects.create(sport=sport, **market_data)
        event = Event.objects.create(sport=sport, **validated_data)
        for selection in selections:
            Selection.objects.create(event=event, market=market, **selection)
        return event


class EventSerializerFilter(serializers.ModelSerializer):
    """
    Class used for displaying filtered events only
    """
    class Meta:
        model = Event
        fields = ['id', 'url', 'name', 'start_time']
        
class MarketSerializerDisplay(serializers.ModelSerializer):
    """
    Class used for GET method only.
    """
    selections = serializers.SerializerMethodField()
    id = serializers.IntegerField()
    
    def __init__(self, instance=None, data=empty,event_id=None, **kwargs):
        """
        Function was overriden in order to get the event(match) id. This was done for supplying only the
        selections with the corresponding event id
        """
        self.instance = instance
        if data is not empty:
            self.initial_data = data
        self.event_id = event_id
        self.partial = kwargs.pop('partial', False)
        self._context = kwargs.pop('context', {})
        kwargs.pop('many', None)
        super(MarketSerializerDisplay, self).__init__(**kwargs)
    
    class Meta:
        model = Market
        fields = ['id', 'name', 'selections']
        depth = 1

    def get_selections(self, obj):
        """
        method used here: selections = serializers.SerializerMethodField()
        The selections are filtered and only the one with the passed event id are returned
        """
        selection = Selection.objects.filter(event=self.event_id)
        serializer = SelectionSerializer(instance=selection, many=True)
        return serializer.data

class EventSerializerDisplay(serializers.ModelSerializer):
    """
    Class used for GET method of the event
    """
    sport = SportSerializer()
    id = serializers.IntegerField(required=True)
    markets = serializers.SerializerMethodField()

    def get_markets(self, obj):
        market = Market.objects.all()
        serializer= MarketSerializerDisplay(instance=market, many=True, event_id=obj.id)
        return serializer.data
    
    class Meta:
        model = Event
        fields = ['id','url', 'name', 'start_time', 'sport', 'markets']
        depth = 1
