from django.db import models
from django.db.models.functions import Lower
from authentication.models import CustomUser


# Create your models here.
class Movie(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255, default='')
    year= models.CharField(max_length=255, default='')  
    place= models.CharField(max_length=255, default='')
    crew= models.CharField(max_length=255, default='')
    ratings= models.CharField(max_length=255, default='')
    votes= models.CharField(max_length=255, default='')
    links = models.CharField(max_length=255, default='')
    title_unique_id = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return super().__str__()

    def last_updated(self):
        return self.updated_at

    def get_all(self):
        return self.objects.all()

    def get_avg_rating(self):
        return self.ratings


WATCH_CHOICES = (
    ('watch_list', 'Watch List'),
    ('watched_list', 'Watched List')
)

class Watch(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    action = models.CharField(max_length=20, choices=WATCH_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_watch_list(self, cls, user):
        return cls.object.filter(user=user, action='watch_list')

    def get_watched_list(self, user):
        return self.object.filter(user=user, action='watched_list')