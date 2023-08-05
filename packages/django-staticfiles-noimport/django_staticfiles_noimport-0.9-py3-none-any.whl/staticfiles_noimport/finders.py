import os
import importlib

from django.contrib.staticfiles.finders import (
    AppDirectoriesFinder as BuiltInAppDirectoriesFinder,
)

from django.conf import settings


class AppDirectoriesNoImportFinder(BuiltInAppDirectoriesFinder):
    """Finder that emulates AppDirectoriesFinder but does so
    through importlib-based file inspection instead of relying
    on the Django app registry.

    When used correctly, this allows for staticfiles collection
    without needing a runnable Django application, which in turn
    requires a significant number of environment variables.
    """

    def __init__(self, *args, **kwargs):
        """AppDirectoriesFinders internals relies on two
        instance variables:

        - self.apps: a list of apps
        - self.storages: a dict of app names to storages
        """
        self.apps = []
        self.storages = {}
        for app in settings.INSTALLED_APPS:
            spec = importlib.util.find_spec(app)
            dir_name = os.path.dirname(spec.origin)
            app_storage = self.storage_class(os.path.join(dir_name, self.source_dir))
            if os.path.isdir(app_storage.location):
                self.storages[app] = app_storage
                self.apps.append(app)


__all__ = ["AppDirectoriesNoImportFinder"]
