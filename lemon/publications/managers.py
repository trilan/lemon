from django.db import models

from lemon.publications.querysets import PublicationQuerySet


class PublicationManager(models.Manager):
    
    def expired(self):
        return self.get_query_set().expired()

    def future(self):
        return self.get_query_set().future()

    def enabled(self):
        return self.get_query_set().enabled()

    def disabled(self):
        return self.get_query_set().disabled()
    
    def unpublished(self):
        return self.get_query_set().unpublished()
    
    def published(self):
        return self.get_query_set().published()
    
    def get_query_set(self):
        return PublicationQuerySet(self.model, using=self._db)
