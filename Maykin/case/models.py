from django.db import models

# Create your models here.
class Stad(models.Model):
    naam = models.CharField(max_length=100)
    achtergrond_afbeelding = models.CharField(max_length=100, blank=True, null=True) 

    def __str__(self):
        return self.naam

class Hotel(models.Model):
    naam = models.CharField(max_length=100)
    stad = models.ForeignKey(Stad, on_delete=models.CASCADE)

    def __str__(self):
        return self.naam
