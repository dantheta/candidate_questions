from django.db import models

class Constituency(models.Model):
    constituency_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=64)
