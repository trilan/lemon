# -*- coding: utf-8 -*-

from django.core.management.base import NoArgsCommand

from lemon import sitemaps
from lemon.sitemaps.models import Item


class Command(NoArgsCommand):

    help = 'Sync sitemap.xml with all registered models'

    def handle_noargs(self, **options):
        print 'Starting sitemap.xml synchronization with all registered models.'
        sitemaps.autodiscover()
        for model, sitemap in sitemaps.site._registry.items():
            print 'Syncing %s.%s model.' % (model._meta.app_label, model.__name__)
            self.sync_sitemap(model, sitemap)
        print 'All objects with `get_absolute_url` method was synced.',
        print 'Removing orphaned sitemap.xml items.'
        self.remove_orphaned()
        print 'Done.'

    def sync_sitemap(self, model, sitemap):
        for obj in model.objects.all():
            try:
                item = Item.objects.get_for_content_object(obj)
            except Item.DoesNotExist:
                if sitemap.url_path(obj):
                    item = Item(content_object=obj)
                    item.save()
                    sites = ', '.join([s.domain for s in item.sites.all()])
                    print '  sitemap.xml item for %s (%s) was created.' % (item.url_path, sites)
            else:
                item.update_url_path()
                item.update_language()
                item.update_sites()
                sites = ', '.join([s.domain for s in item.sites.all()])
                print '  sitemap.xml item for %s (%s) was updated.' % (item.url_path, sites)

    def remove_orphaned(self):
        for item in Item.objects.all():
            if item.content_type and item.object_id:
                if not item.content_object:
                    sites = ', '.join([s.domain for s in item.sites.all()])
                    print '  sitemap.xml item for %s (%s) deleted.' % (item.url_path, sites)
                    item.delete()
