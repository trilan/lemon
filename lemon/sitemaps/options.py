from django.contrib.sites.models import Site
from django.db.models import FieldDoesNotExist, ForeignKey, ManyToManyField


class ModelSitemap(object):

    sites_field_name = None

    def sites_field_class(self, model):
        try:
            return model._meta.get_field_by_name(
                self.sites_field_name)[0].__class__
        except FieldDoesNotExist:
            return None

    def sites(self, obj):
        if not self.sites_field_name:
            return Site.objects.all()
        sites_field_class = self.sites_field_class(obj.__class__)
        if sites_field_class is ForeignKey:
            return [getattr(obj, self.sites_field_name)]
        if sites_field_class is ManyToManyField:
            return getattr(obj, self.sites_field_name).all()
        return []

    def url_path(self, obj):
        try:
            return obj.get_absolute_url()
        except Exception:
            return None
