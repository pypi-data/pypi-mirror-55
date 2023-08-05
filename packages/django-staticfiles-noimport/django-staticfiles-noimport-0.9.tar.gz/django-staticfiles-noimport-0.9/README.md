# Django Staticfiles Noimport

[![Build Status](https://travis-ci.org/roverdotcom/django-staticfiles-noimport.svg?branch=master)](https://travis-ci.org/roverdotcom/django-staticfiles-noimport)

django-staticfiles-import exists to allow Django's
`collectstatic` management command to run with the
bare minimum of environment variables so it can be
run inside a `docker build` step such that the produced
container is self-contained.

This approach allows typical runtime initialization to
verify all required runtime environment variables are
defined and provides an alternative entrypoint for just
the `collectstatic` and `findstatic` commands.

Specifically, this project allows for Django apps
with `static/` directories that expect you to use the
enabled-by-default `AppDirectoriesFinder`.

## Requirements & Constraints

Utilizing this package requires accepting a handful of
constraints that are acceptable in our environment:

- Static assets will be served at the same path in all
  environments (i.e. `STATIC_URL` doesn't vary per
  environment.)
- Django "apps" may not manipulate any static
  file handling behaviors during app initialization.
- `INSTALLED_APPS` must reference app names as strings,
  as opposed to importing an `AppConfig` directly.

## Setup

1. Ensure you have an `os.environ`-agnostic settings module.
   - This may be achieved by creating a simple `settings/apps.py` module that is imported from your primary settings with glob syntax like: `from .apps import *` and a `settings/static.py` that imports it as well.
   - Somewhere in that settings chain you must define `SECRET_KEY` which is the one required non-staticfiles related setting.
2. Use the provided `staticfiles_noimport.finders.AppDirectoriesNoImportFinder` in your `STATICFILES_FINDERS` settings. (See included example.)
3. Use `collectstatic` and `findstatic` directly without using the typical `manage.py` entrypoint. You'll need to inject your static-specific settings (e.g., `DJANGO_SETTINGS_MODULE=settings.static`) for things to work as expected.

## Example Usage

```python
# settings/apps.py
INSTALLED_APPS = (
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.admin",
    ...
    ...
    "yourappone",
    "yourapptwo",
)

# settings/static.py
from .apps import *

STATIC_ROOT = "/static/foobar/"
STATIC_URL = "/static/foobar/"

STATICFILES_DIRS = (
    "/some/resolved/path/static",
)

STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "staticfiles_noimport.finders.AppDirectoriesNoImportFinder"
)

STATICFILES_STORAGE = "django.contrib.staticfiles.storage.ManifestStaticFilesStorage"
```

Running collectstatic:

```bash
$ DJANGO_SETTINGS_MODULE=myproject.settings.static collectstatic
```
