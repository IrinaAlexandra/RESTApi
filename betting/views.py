
from .models import Event, Selection
from .serializers import EventSerializer, EventSerializerFilter, SelectionSerializer, EventSerializerDisplay
from rest_framework import generics
from rest_framework import mixins
from rest_framework.response import Response
from rest_framework import status

# Create your views here.

class EventListPost(generics.ListCreateAPIView, mixins.UpdateModelMixin, mixins.ListModelMixin, mixins.CreateModelMixin):
    """
    Class used For the POST method only
    """
    queryset = {}
    def create(self, request, *args, **kwargs):
        """
        Function that checks the message type sent.
        """
        if request.data['message_type'] == 'NewEvent':
            serializer = self.get_serializer(data=request.data['event'])
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(request.data['event'], status=status.HTTP_201_CREATED, headers=headers)
        
        if request.data['message_type'] == 'UpdateOdds':
            for selection in request.data['event']['markets'][0]['selections']:
                instance = self.get_object(selection)
                instance.odds = selection.get('odds')
                instance.save()
                return Response(request.data['event'], status=status.HTTP_201_CREATED)                
    
    def get_object(self, selection):
        """
        Function needed for the update functionality. In order to perform the update of the odds,
        the selection object is needed. This function provides this to the create function above
        """
        if 'message_type' in self.request.data and self.request.data['message_type'] == 'UpdateOdds':
            selection_id = selection.get('id')
            return Selection.objects.get(pk=selection_id)
        else:
            return super(EventList, self).get_object()

    def get_serializer_class(self):
        """
        Function that passes different serializer classes depending of the message type
        """
        if 'message_type' in self.request.data:
            if self.request.data['message_type'] == 'NewEvent':
                return EventSerializer    
            elif self.request.data['message_type'] == 'UpdateOdds':
                return SelectionSerializer
        else:
            return EventSerializer

class EventListGet(generics.ListAPIView):
    """
    List View class for the GET method
    """
    queryset = Event.objects.all()
    serializer_class = EventSerializerDisplay
    
class EventDetail(generics.RetrieveAPIView):
    """
    Detail View class for the GET method
    """
    queryset = Event.objects.all()
    serializer_class = EventSerializerDisplay

class EventOrderBy(generics.ListCreateAPIView):
    """
    Order by View class
    """
    serializer_class = EventSerializerFilter
    def get_queryset(self):
        """
        function checks for the ordering argument and orders the records based on that
        """
        queryset = Event.objects.all()
        order_by = self.request.query_params.get('ordering', None)
        if order_by is not None:
            queryset = queryset.order_by(order_by)
        return queryset

class EventFilter(generics.ListCreateAPIView):
    """
    Search by name View class
    """
    serializer_class = EventSerializerFilter
    def get_queryset(self):
        """
        function checks the name argument and retrieves the record with that name
        :return:
        """
        queryset = Event.objects.all()
        filter_by = self.request.query_params.get('name', None)
        if filter_by is not None:
            queryset = Event.objects.filter(name=filter_by)
        return queryset

