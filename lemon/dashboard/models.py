from django.contrib.auth.models import User
from django.db import models
from django.db.models.query import QuerySet
from django.utils import simplejson as json


COLUMN_CHOICES = (
    ('left', 'left'),
    ('right', 'right'),
)


class WidgetInstanceQuerySet(QuerySet):

    def to_raw(self):
        queryset = self._clone()
        return [widget_instance.to_raw() for widget_instance in queryset]

    def to_json(self):
        return json.dumps(self.to_raw())


class WidgetInstanceManager(models.Manager):

    def adjust_column(self, user, dashboard, column, respect=None):
        queryset = self.filter(user=user, dashboard=dashboard, column=column)
        key = lambda o: (o.position, 1 if o == respect else 0)
        for position, widget_instance in enumerate(sorted(queryset, key=key)):
            widget_instance.position = position
            widget_instance.save()

    def adjust(self, user, dashboard, respect=None):
        self.adjust_column(user, dashboard, "left", respect)
        self.adjust_column(user, dashboard, "right", respect)

    def to_raw(self):
        return self.get_query_set().to_raw()

    def to_json(self):
        return self.get_query_set().to_json()

    def get_query_set(self):
        return WidgetInstanceQuerySet(self.model, using=self._db)


class WidgetInstance(models.Model):

    user = models.ForeignKey(User)
    dashboard = models.CharField(max_length=50)
    widget = models.CharField(max_length=50)
    column = models.CharField(max_length=5, choices=COLUMN_CHOICES)
    position = models.PositiveIntegerField()

    objects = WidgetInstanceManager()

    class Meta:
        unique_together = ('user', 'dashboard', 'widget')

    def to_raw(self):
        return {
            'id': self.pk,
            'widget': self.widget,
            'column': self.column,
            'position': self.position,
        }

    def to_json(self):
        return json.dumps(self.to_raw())
