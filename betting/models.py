from django.db import models

# Create your models here.
class Sport(models.Model):
    name = models.CharField(max_length = 100, blank = False)
	
    def __str__(self):
        return self.name


class Event(models.Model):
    #also referred to as match inside the implementation details
    
    name = models.CharField(max_length = 100, blank = False)
    start_time = models.DateTimeField(auto_now_add=True)
    sport = models.ForeignKey(Sport,related_name='sport', on_delete = models.CASCADE)
    
    def __str__(self):
        return self.name
    
    #needed in order to return the markets when displaying event data
    @property
    def markets(self):
        return  Market.objects.filter(sport=self.sport)
    
class Market(models.Model):
	
    name = models.CharField(max_length = 100, blank = False)
    sport = models.ForeignKey(Sport, related_name='markets',on_delete = models.CASCADE)
	
    def __str__(self):
        return self.name

    #needed in order to return the selections when displaying event data
    @property
    def selections(self):
        return Selection.objects.filter(market=self.id, event= Event.object)

class Selection(models.Model):
	
    name = models.CharField(max_length = 100, blank = False)
    odds = models.DecimalField(max_digits = 5, decimal_places = 2)
    market = models.ForeignKey(Market,related_name='selections', on_delete = models.CASCADE)
    event = models.ForeignKey(Event, related_name='event', on_delete = models.CASCADE) #assuming selections are bound to events(matches)

    def __str__(self):
        return self.name

