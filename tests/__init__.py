import os
import sys
from django.conf import settings


if not settings.configured:
    settings.configure(
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
            }
        },
        INSTALLED_APPS = (
            'lemon.dashboard',
            'lemon.extradmin',

            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'django.contrib.sites',
            'django.contrib.messages',
            'django.contrib.admin',

            'lemon.filebrowser',
            'lemon.metatags',
            'lemon.pages',
            'lemon.robots',
            'lemon.sitemaps',

            'south',
            'intellipages',
        ),
        SITE_ID = 1,
        STATIC_URL = '',
        LEMON_MEDIA_PREFIX = '/lemonmedia/',
        UPLOAD_TO = 'uploads',
        ROOT_URLCONF = '',
        DEBUG = False,
        MIDDLEWARE_CLASSES = (
            'django.middleware.common.CommonMiddleware',
            'django.contrib.sessions.middleware.SessionMiddleware',
            'django.middleware.csrf.CsrfViewMiddleware',
            'django.contrib.auth.middleware.AuthenticationMiddleware',
            'django.contrib.messages.middleware.MessageMiddleware',
            'lemon.utils.middleware.sites.RequestSiteMiddleware',
            'lemon.pages.middleware.PageMiddleware'
        ),
        TEMPLATE_LOADERS = (
            'django.template.loaders.filesystem.Loader',
            'django.template.loaders.app_directories.Loader',
        ),
        TEMPLATE_DIRS = (
            os.path.join(os.path.abspath(os.path.dirname(__file__)), 'templates'),
        ),
        SOUTH_TESTS_MIGRATE = False
    )

TEST_APPS = (
    'lemon.dashboard',
    'lemon.extradmin',
    'lemon.robots',
    'lemon.sitemaps',
)


def main():
    from django.test.utils import get_runner
    from south.management.commands import patch_for_test_db_setup

    patch_for_test_db_setup()
    test_runner = get_runner(settings)(interactive=False)
    failures = test_runner.run_tests([app.split('.')[-1] for app in TEST_APPS])
    sys.exit(failures)


if __name__ == '__main__':
    main()
