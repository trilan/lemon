from django.core.urlresolvers import reverse
from django.test import TestCase

from lemon.sitemaps.models import Item


class SiteMapViewTestCase(TestCase):

    fixtures = ['test_sitemaps.json']
    urls = 'lemon.sitemaps.tests.urls'

    def test_response(self):
        response = self.client.get('/sitemap.xml')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-type'], 'application/xml')

        site_map_item_list = response.context.get('object_list')
        self.assertTrue(all(isinstance(item, Item) for item in site_map_item_list))

    def test_filter_by_site(self):
        response = self.client.get('/sitemap.xml', HTTP_HOST='second.example.com')
        self.assertEqual(response.status_code, 200)

        site_map_item_list = response.context.get('object_list')
        self.assertEqual(len(site_map_item_list), 1)
        self.assertEqual(site_map_item_list[0].pk, 2)

    def test_empty_result(self):
        response = self.client.get('/sitemap.xml', HTTP_HOST='third.example.com')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context.get('object_list')), 0)

    def test_url_name(self):
        self.assertEqual(reverse('sitemap_xml'), '/sitemap.xml')
