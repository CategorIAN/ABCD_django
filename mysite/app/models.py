from django.db import models

class Person(models.Model):
    name = models.CharField(primary_key=True, max_length=160)
    email = models.CharField(max_length=160, blank=True, null=True)
    max_hours = models.IntegerField(blank=True, null=True)
    status = models.CharField(max_length=160, blank=True, null=True)
    earliest_invite = models.CharField(max_length=160, blank=True, null=True)
    latest_invite = models.CharField(max_length=160, blank=True, null=True)
    frequency = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'person'