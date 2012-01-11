# -*- coding: utf-8 -*-

from django.core.management.base import NoArgsCommand

from lemon import metatags
from lemon.metatags.models import Page


class Command(NoArgsCommand):

    help = 'Sync metatags with all registered models'

    def handle_noargs(self, **options):
        from django.contrib import admin
        admin.autodiscover()

        print 'Starting metatags synchronisation with all registered models.'
        for model in metatags.site._registry:
            print 'Syncing %s model.' % model._meta
            self.sync_metatags(model)
        print 'All objects with `get_absolute_url` method was synced.',

        print 'Removing orphaned metatags.'
        self.remove_orphaned()
        print 'Done.'

    def sync_metatags(self, model):
        for obj in model.objects.all():
            try:
                page = Page.objects.get_for_content_object(obj)
            except Page.DoesNotExist:
                continue
            page.update_url_path()
            page.update_language()
            page.update_sites()
            sites = ', '.join([s.domain for s in page.sites.all()])
            print '  Metatags for %s (%s) was updated.' % (page.url_path, sites)

    def remove_orphaned(self):
        for page in Page.objects.all():
            if not page.has_content_object() or page.content_object:
                continue
            url_path = path.url_path
            sites = ', '.join([s.domain for s in page.sites.all()])
            page.delete()
            print '  Metatags for %s (%s) was deleted.' % (url_path, sites)
