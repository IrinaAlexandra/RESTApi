from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from betting import views

urlpatterns = [
    path('betting/', views.EventList.as_view()), #Get all events(matches). Here to also send the post method with the new even
    path('betting/<int:pk>/', views.EventDetail.as_view(), name='event-detail'),
    path('betting/event/football/', views.EventOrderBy.as_view()),# add your ordering= paramaer here
    path('betting/event/', views.EventFilter.as_view()),# add ?name= paramer here
    path('betting/selection/update/<int:pk>', views.SelectionDetail.as_view()) #work in progress
]

urlpatterns = format_suffix_patterns(urlpatterns)

