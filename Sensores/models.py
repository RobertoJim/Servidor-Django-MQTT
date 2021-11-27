from django.db import models

# Create your models here.


class Temperatura(models.Model):

    temperatura = models.FloatField()
    hora = models.FloatField()
    

class Humedad(models.Model):

    humedad = models.FloatField()
    hora = models.FloatField()