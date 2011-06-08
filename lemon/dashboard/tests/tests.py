from django.contrib.auth.models import User
from django.core.exceptions import ImproperlyConfigured
from django.test import TestCase, RequestFactory
from django.utils import simplejson as json

from lemon.dashboard.models import WidgetInstance

from .admin import first_dashboard, second_dashboard
from .dashboard import FirstHelpWidget
from .views import AppAdminView


class DashboardTest(TestCase):

    fixtures = ['dashboard_admin_test.json']

    def test_registry(self):
        self.assertItemsEqual(
            first_dashboard._registry.keys(),
            ['first_help_widget', 'second_help_widget'])

    def test_registered_widget(self):
        widget_instance = first_dashboard._registry['first_help_widget']
        self.assertIsInstance(widget_instance, FirstHelpWidget)
        self.assertEqual(widget_instance.label, 'first_help_widget')

    def test_queryset(self):
        user = User.objects.get(pk=1)
        queryset = first_dashboard.get_queryset({'user': user}).order_by('pk')
        self.assertQuerysetEqual(queryset, [1, 2], lambda x: x.pk)


class AppAdminMixinTest(TestCase):

    def setUp(self):
        self.factory = RequestFactory()

    def test_app_admin_required(self):
        view = AppAdminView.as_view()
        request = self.factory.get('/')
        self.assertRaises(ImproperlyConfigured, view, request)


class AdminSiteTest(TestCase):

    urls = 'lemon.dashboard.tests.urls'
    fixtures = ['dashboard_admin_test.json']

    def setUp(self):
        self.client.login(username='admin', password='qwerty')

    def tearDown(self):
        self.client.logout()

    def test_index_view(self):
        response = self.client.get('/first_admin/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response, '<div id="dashboard" class="dashboard"></div>')


class DashboardAdminTest(TestCase):

    urls = 'lemon.dashboard.tests.urls'
    fixtures = ['dashboard_admin_test.json']

    def setUp(self):
        self.client.login(username='admin', password='qwerty')
        self.user = User.objects.get(pk=1)

    def tearDown(self):
        self.client.logout()

    def test_widget_list(self):
        response = self.client.get('/first_admin/dashboard/widgets')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-type'], 'application/json')

        data = json.loads(response.content)
        self.assertEqual(
            data, [w.to_raw() for w in first_dashboard._registry.values()])

    def test_widget_instance_list(self):
        response = self.client.get('/first_admin/dashboard/widget_instances')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-type'], 'application/json')

        data = json.loads(response.content)
        self.assertItemsEqual([o['id'] for o in data], [1, 2])

    def test_create_widget_instance(self):
        response = self.client.post(
            path='/first_admin/dashboard/widget_instances',
            data=json.dumps({'column': 'left', 'position': 0}),
            content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response['Content-type'], 'application/json')

        data = json.loads(response.content)
        self.assertEqual(data['column'], 'left')
        self.assertEqual(data['position'], 0)

        widget_instance = WidgetInstance.objects.get(pk=data['id'])
        self.assertEqual(widget_instance.user, self.user)
        self.assertEqual(widget_instance.dashboard, u'first_dashboard')

    def test_update_widget_instance(self):
        response = self.client.put(
            path='/first_admin/dashboard/widget_instances/1',
            data=json.dumps({'column': 'right', 'position': 0}),
            content_type='application/json')
        self.assertEqual(response.status_code, 204)
        self.assertEqual(response['Content-type'], 'application/json')

        widget_instance = WidgetInstance.objects.get(pk=1)
        self.assertEqual(widget_instance.column, 'right')
        self.assertEqual(widget_instance.position, 0)

    def test_update_widget_instance_with_wrong_dashboard(self):
        response = self.client.put(
            path='/second_admin/dashboard/widget_instances/1',
            data=json.dumps({'column': 'right', 'position': 0}),
            content_type='application/json')
        self.assertEqual(response.status_code, 404)

    def test_update_widget_instance_with_wrong_user(self):
        response = self.client.put(
            path='/second_admin/dashboard/widget_instances/4',
            data=json.dumps({'column': 'right', 'position': 0}),
            content_type='application/json')
        self.assertEqual(response.status_code, 404)

    def test_delete_widget_instance(self):
        response = self.client.delete('/first_admin/dashboard/widget_instances/1')
        self.assertEqual(response.status_code, 204)
        self.assertEqual(response['Content-type'], 'application/json')

        queryset = WidgetInstance.objects.filter(pk=1)
        self.assertFalse(queryset.exists())

    def test_delete_widget_instance_with_wrong_dashboard(self):
        response = self.client.delete('/second_admin/dashboard/widget_instances/1')
        self.assertEqual(response.status_code, 404)

    def test_delete_widget_instance_with_wrong_user(self):
        response = self.client.delete('/second_admin/dashboard/widget_instances/4')
        self.assertEqual(response.status_code, 404)
