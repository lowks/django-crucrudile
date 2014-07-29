DATABASES = {
    u'default': {
        u'ENGINE': u'django.db.backends.sqlite3',
        u'NAME': u':memory:',
    }
}
INSTALLED_APPS = (
    u'django.contrib.contenttypes',
    u'django.contrib.auth',
    u'django_crucrudile',
    u'tests',
)

MARKITUP_FILTER = (u'markdown.markdown', {u'safe_mode': True})
ROOT_URLCONF = u'tests.urls'
USE_TZ = True
SECRET_KEY = u'so long and thanks for all the fish'

