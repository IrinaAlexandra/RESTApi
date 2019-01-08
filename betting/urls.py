from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from betting import views

urlpatterns = [
    path('betting/submit', views.EventListPost.as_view()), #view for posting new events or odds updates
    path('betting/', views.EventListGet.as_view()), #get all the events(matches)
    path('betting/<int:pk>/', views.EventDetail.as_view(), name='event-detail'), #get match by id
    path('betting/event/football/', views.EventOrderBy.as_view()), #get matches with the ability to order by
    path('betting/event/', views.EventFilter.as_view()), #get matches with the ability to search by name
]

urlpatterns = format_suffix_patterns(urlpatterns)

