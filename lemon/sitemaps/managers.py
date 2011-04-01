from django.db import models
from lemon.sitemaps.querysets import ItemQuerySet


class ItemManager(models.Manager):

    def get_query_set(self):
        return ItemQuerySet(self.model, using=self._db)

    def get_for_content_object(self, content_object):
        return self.get_query_set().get_for_content_object(content_object)

    def filter_by_content_object(self, content_object):
        return self.get_query_set().filter_by_content_object(content_object)
