from django.contrib.auth.models import User
from django.core.exceptions import ImproperlyConfigured
from django.test import TestCase, RequestFactory
from django.utils import simplejson as json

from lemon.dashboard.forms import CreateWidgetInstanceForm
from lemon.dashboard.models import WidgetInstance

from .admin import first_dashboard, second_dashboard
from .dashboard import FirstHelpWidget
from .views import AppAdminView


class DashboardTest(TestCase):

    fixtures = ['dashboard_admin_test.json']

    def test_registry(self):
        self.assertItemsEqual(
            first_dashboard._registry.keys(),
            ['first_help_widget', 'second_help_widget', 'third_help_widget'])

    def test_registered_widget(self):
        widget_instance = first_dashboard._registry['first_help_widget']
        self.assertIsInstance(widget_instance, FirstHelpWidget)
        self.assertEqual(widget_instance.label, 'first_help_widget')

    def test_queryset(self):
        queryset = first_dashboard.get_queryset(user=1).order_by('pk')
        self.assertQuerysetEqual(queryset, [1, 2], lambda x: x.pk)

    def test_used_widget_labels(self):
        self.assertItemsEqual(
            first_dashboard.get_used_widget_labels(user=1),
            ['first_help_widget', 'second_help_widget'])

    def test_registered_widgets(self):
        self.assertItemsEqual(first_dashboard.get_registered_widgets(), [
            first_dashboard._registry['first_help_widget'],
            first_dashboard._registry['second_help_widget'],
            first_dashboard._registry['third_help_widget'],
        ])
        self.assertItemsEqual(second_dashboard.get_registered_widgets(), [
            second_dashboard._registry['third_help_widget'],
        ])

    def test_available_widgets(self):
        self.assertItemsEqual(
            first_dashboard.get_available_widgets(user=1),
            [first_dashboard._registry['third_help_widget']])


class CreateWidgetInstanceFormTest(TestCase):

    fixtures = ['dashboard_admin_test.json']

    def setUp(self):
        self.user = User.objects.get(pk=1)
        self.data = {
            'widget': 'third_help_widget',
            'column': 'left',
            'position': 0,
        }

    def test_instance(self):
        form = CreateWidgetInstanceForm(first_dashboard, self.user)
        self.assertIs(form.dashboard, first_dashboard)
        self.assertIs(form.user, self.user)

    def test_valid_data(self):
        form = CreateWidgetInstanceForm(first_dashboard, self.user, self.data)
        self.assertTrue(form.is_valid())

    def test_widget_not_registered(self):
        data = self.data.copy()
        data.update(widget='not_registered')
        form = CreateWidgetInstanceForm(first_dashboard, self.user, data)
        self.assertFalse(form.is_valid())
        self.assertIn('widget', form.errors)
        self.assertEqual(len(form.errors['widget']), 1)
        self.assertIn('is not registered', form.errors['widget'][0])

    def test_widget_not_available(self):
        data = self.data.copy()
        data.update(widget='first_help_widget')
        form = CreateWidgetInstanceForm(first_dashboard, self.user, data)
        self.assertFalse(form.is_valid())
        self.assertIn('widget', form.errors)
        self.assertEqual(len(form.errors['widget']), 1)
        self.assertIn('is not available', form.errors['widget'][0])

    def test_save(self):
        form = CreateWidgetInstanceForm(first_dashboard, self.user, self.data)
        form.is_valid()
        instance = form.save()
        self.assertIsNotNone(instance)
        self.assertEqual(instance.dashboard, first_dashboard.label)
        self.assertEqual(instance.user, self.user)


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
            data=json.dumps({
                'widget': 'third_help_widget',
                'column': 'left',
                'position': 0}),
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

    def test_update_widget_instance_with_invalid_column(self):
        response = self.client.put(
            path='/first_admin/dashboard/widget_instances/1',
            data=json.dumps({'column': 'center', 'position': 0}),
            content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_update_widget_instance_with_invalid_position(self):
        response = self.client.put(
            path='/first_admin/dashboard/widget_instances/1',
            data=json.dumps({'column': 'left', 'position': 'abc'}),
            content_type='application/json')
        self.assertEqual(response.status_code, 400)

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
