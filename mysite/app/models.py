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

    def __str__(self):
        return self.name

class Forms(models.Model):
    name = models.CharField(primary_key=True, max_length=160)
    updated = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'forms'

    def __str__(self):
        return self.name

class FormRequests(models.Model):
    person = models.ForeignKey('Person', models.DO_NOTHING, db_column='person', blank=True, null=True)
    form = models.ForeignKey('Forms', models.DO_NOTHING, db_column='form', blank=True, null=True)
    timestamp = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'form_requests'