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
            'lemon',
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'django.contrib.sites',
            'django.contrib.messages',
            'django.contrib.admin',
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
        ),
        TEMPLATE_LOADERS = (
            'django.template.loaders.filesystem.Loader',
            'django.template.loaders.app_directories.Loader',
        ),
    )


def main():
    from django.test.utils import get_runner

    test_runner = get_runner(settings)(interactive=False)
    failures = test_runner.run_tests(['lemon'])
    sys.exit(failures)


if __name__ == '__main__':
    main()
