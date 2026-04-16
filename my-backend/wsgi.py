import os
import sys
from django.conf import settings

# Configure Django settings
if not settings.configured:
    settings.configure(
        DEBUG=True,
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': os.path.join(os.path.dirname(__file__), 'db.sqlite3'),
            }
        },
        INSTALLED_APPS=[
            'django.contrib.contenttypes',
            'django.contrib.auth',
            'corsheaders',
            'rest_framework',
            'api',
        ],
        MIDDLEWARE=[
            'corsheaders.middleware.CorsMiddleware',
            'django.middleware.common.CommonMiddleware',
        ],
        CORS_ALLOWED_ORIGINS=[
            'https://hmh-8138.github.io',
            'http://localhost:3000',
        ],
        CORS_ALLOW_CREDENTIALS=True,
        SECRET_KEY='django-insecure-your-secret-key-here-change-in-production',
        ROOT_URLCONF='urls',
        TEMPLATES=[{
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [],
            'APP_DIRS': True,
        }],
    )

import django
django.setup()
