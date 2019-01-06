from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from betting import views

urlpatterns = [
    path('betting/', views.EventList.as_view()),
    path('betting/<int:pk>/', views.EventDetail.as_view(), name='event-detail'),
    path('betting/event/football/', views.EventOrderBy.as_view()),
    path('betting/event/', views.EventFilter.as_view()),
    path('betting/selection/update/<int:pk>', views.SelectionDetail.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns)

