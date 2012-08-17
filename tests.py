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
        ROOT_URLCONF = '',
    )


def main():
    from django.test.utils import get_runner

    test_runner = get_runner(settings)(interactive=False)
    failures = test_runner.run_tests(['lemon'])
    sys.exit(failures)


if __name__ == '__main__':
    main()
