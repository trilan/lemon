# -*- coding: utf-8 -*-

from django.core.management.base import NoArgsCommand

from lemon import sitemaps
from lemon.sitemaps.models import Item


class Command(NoArgsCommand):

    help = 'Sync sitemap.xml with all registered models'

    def handle_noargs(self, **options):
        from django.contrib import admin
        admin.autodiscover()

        print 'Starting sitemap.xml synchronization with all registered models.'
        for model in sitemaps.site._registry:
            print 'Syncing %s model.' % model._meta
            self.sync_sitemaps(model)
        print 'All objects with `get_absolute_url` method was synced.',

        print 'Removing orphaned sitemap.xml items.'
        self.remove_orphaned()
        print 'Done.'

    def sync_sitemaps(self, model):
        for obj in model.objects.all():
            try:
                item = Item.objects.get_for_content_object(obj)
            except Item.DoesNotExist:
                if not sitemap.url_path(obj):
                    continue
                item = Item.objects.create(content_object=obj)
                action = 'created'
            else:
                item.update_url_path()
                item.update_language()
                item.update_sites()
                action = 'updated'
            sites = ', '.join([s.domain for s in item.sites.all()])
            print '  sitemap.xml item for %s (%s) was %s.' % (item.url_path, sites, action)

    def remove_orphaned(self):
        for item in Item.objects.all():
            if not item.has_content_object() or item.content_object:
                continue
            url_path = item.url_path
            sites = ', '.join([s.domain for s in item.sites.all()])
            item.delete()
            print '  sitemap.xml item for %s (%s) deleted.' % (url_path, sites)
