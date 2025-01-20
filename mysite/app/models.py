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

class Event(models.Model):
    eventid = models.AutoField(primary_key=True)
    timestamp = models.DateTimeField(blank=True, null=True)
    timespan = models.ForeignKey('Timespan', models.DO_NOTHING, db_column='timespan', blank=True, null=True)
    meal = models.ForeignKey('Meals', models.DO_NOTHING, db_column='meal', blank=True, null=True)
    game = models.ForeignKey('Games', models.DO_NOTHING, db_column='game', blank=True, null=True)
    location = models.ForeignKey('Location', models.DO_NOTHING, db_column='location', blank=True, null=True)
    happened = models.BooleanField(blank=True, null=True)
    event_plan = models.ForeignKey('EventPlan', models.DO_NOTHING, db_column='event_plan', blank=True, null=True)
    week = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'event'

    def __str__(self):
        return f"({self.eventid}) {self.game}@{self.timestamp}"

class EventPlan(models.Model):
    name = models.CharField(primary_key=True, max_length=160)
    month = models.ForeignKey('Month', models.DO_NOTHING, db_column='month', blank=True, null=True)
    year = models.IntegerField(blank=True, null=True)
    game = models.ForeignKey('Games', models.DO_NOTHING, db_column='game', blank=True, null=True)
    duration = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'event_plan'

class Games(models.Model):
    name = models.CharField(primary_key=True, max_length=160)
    other = models.BooleanField(blank=True, null=True)
    weight = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'games'

    def __str__(self):
        return self.name

class Invitation(models.Model):
    timestamp = models.DateTimeField(blank=True, null=True)
    person = models.ForeignKey('Person', models.DO_NOTHING, db_column='person', blank=True, null=True)
    event = models.ForeignKey(Event, models.DO_NOTHING, db_column='event', blank=True, null=True)
    response = models.BooleanField(blank=True, null=True)
    plus_ones = models.IntegerField(blank=True, null=True)
    result_opts = [(x, x) for x in ['Going', 'Passed', 'Flaked', 'Waiting', 'To Redeem', 'Redeemed']]
    result = models.CharField(choices=result_opts, null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'invitation'

class Location(models.Model):
    name = models.CharField(primary_key=True, max_length=160)
    other = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'location'

class Meals(models.Model):
    name = models.CharField(primary_key=True, max_length=160)
    other = models.BooleanField(blank=True, null=True)
    weight = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'meals'

class Month(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=160, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'month'

class Timespan(models.Model):
    name = models.CharField(primary_key=True, max_length=160)

    class Meta:
        managed = False
        db_table = 'timespan'