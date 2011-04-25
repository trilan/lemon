from django.contrib.auth.models import User
from django.db import models
from django.utils import simplejson as json

from lemon.dashboard.settings import CONFIG


def _get_default_data():
    columns = []
    for column in CONFIG['STATE']:
        cells = []
        for cell in column:
            cells.append({'name': cell, 'state': {}})
        columns.append(cells)
    return json.dumps({'columns': columns})


class DashboardStateManager(models.Manager):

    def get_for_user(self, user):
        state, created = self.get_or_create(user=user)
        return state


class DashboardState(models.Model):

    user = models.OneToOneField(User)
    data = models.TextField(default=_get_default_data())

    objects = DashboardStateManager()

    def has_widget(self, name):
        data = json.loads(self.data)
        for column in data['columns']:
            for cell in column:
                if cell['name'] == name:
                    return True
        return False

    def add_widget(self, column, name, commit=True):
        data = json.loads(self.data)
        data['columns'][column].insert(0, {'name': name, 'state': {}})
        self.data = json.dumps(data)
        if commit:
            self.save()

    def delete_widget(self, name, commit=True):
        data = json.loads(self.data)
        new_columns = []
        for column in data['columns']:
            new_column = []
            for cell in column:
                if cell['name'] != name:
                    new_column.append(cell)
            new_columns.append(new_column)
        data['columns'] = new_columns
        self.data = json.dumps(data)
        if commit:
            self.save()
