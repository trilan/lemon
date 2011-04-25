from django.test import TestCase
from lemon.robots.models import File


class RobotsTestCase(TestCase):

    fixtures = ['test_robots.json']
    urls = 'lemon.robots.tests.urls'

    def test_response(self):
        response = self.client.get('/robots.txt')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-type'], 'text/plain')

        robots_txt_file = response.context.get('object')
        self.assertTrue(isinstance(robots_txt_file, File))

    def test_filter_by_site(self):
        response = self.client.get('/robots.txt', HTTP_HOST='second.example.com')
        self.assertEqual(response.status_code, 200)

        robots_txt_file = response.context.get('object')
        self.assertEqual(robots_txt_file.content, 'second.example.com')

    def test_default_template(self):
        response = self.client.get('/robots.txt', HTTP_HOST='third.example.com')
        self.assertEqual(response.status_code, 200)

        robots_txt_file = response.context.get('object')
        self.assertTrue(robots_txt_file is None)
