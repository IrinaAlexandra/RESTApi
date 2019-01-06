
from .models import Event, Sport, Market, Selection
from .serializers import EventSerializer, SportSerializer, EventSerializerFilter, SelectionSerializer
from rest_framework import generics
from rest_framework import mixins
from rest_framework.response import Response
from rest_framework import status

# Create your views here.

class EventList(generics.ListCreateAPIView, mixins.ListModelMixin, mixins.CreateModelMixin):
    queryset = Event.objects.all()

    def create(self, request, *args, **kwargs):
        if request.data['message_type'] == 'NewEvent':
            serializer = self.get_serializer(data=request.data['event'])
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    

    def get_serializer_class(self):
        if 'message_type' in self.request.data:
            if self.request.data['message_type'] == 'NewEvent':
                return EventSerializer    
            elif self.request.data['message_type'] == 'UpdateOdds':
                return SelectionSerializer
        else:
            return EventSerializer
    
class SelectionDetail(generics.UpdateAPIView):
    queryset = Selection.objects.all()
    serializer_class = SelectionSerializer
    def create(self, request, *args, **kwargs):
        if request.data['message_type'] == 'UpdateOdds':
            for selection in request.data['event']['markets'][0]['selections']:
                serializer = self.get_serializer(data=selection.get('odds'))
                serializer.is_valid(raise_exception=True)
                self.perform_create(serializer)
                headers = self.get_success_headers(serializer.data)
                return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    def get_serializer(self, *args, **kwargs):
        kwargs['partial'] = True
        return super(SelectionDetail, self).get_serializer(*args, **kwargs)

class EventDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

class EventOrderBy(generics.ListCreateAPIView):
    serializer_class = EventSerializerFilter
    
    def get_queryset(self):
        queryset = Event.objects.all()
        order_by = self.request.query_params.get('ordering', None)
        if order_by is not None:
            queryset = queryset.order_by(order_by)
        return queryset

class EventFilter(generics.ListCreateAPIView):
    serializer_class = EventSerializerFilter
    
    def get_queryset(self):
        queryset = Event.objects.all()
        filter_by = self.request.query_params.get('name', None)
        if filter_by is not None:
            queryset = Event.objects.filter(name=filter_by)
        return queryset

