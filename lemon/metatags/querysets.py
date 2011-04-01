from django.contrib.contenttypes.models import ContentType
from django.db.models.query import QuerySet


class PageQuerySet(QuerySet):

    def get_for_content_object(self, content_object):
        return self.filter_by_content_object(content_object).get()

    def filter_by_content_object(self, content_object):
        content_type = ContentType.objects.get_for_model(content_object)
        return self.filter(content_type=content_type, object_id=content_object.pk)
