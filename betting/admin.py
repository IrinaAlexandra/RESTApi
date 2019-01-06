from django.contrib import admin
from .models import Sport, Event, Market, Selection

admin.site.register([Sport, Event, Market, Selection])
# Register your models here.
