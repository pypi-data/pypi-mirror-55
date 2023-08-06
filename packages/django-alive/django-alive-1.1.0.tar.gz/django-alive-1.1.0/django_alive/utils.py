from django.conf import settings
from django.utils.module_loading import import_string

from . import HealthcheckFailure

# Ignore typing on Python <3.5
try:
    from typing import List
except ImportError:
    pass


DEFAULT_ALIVE_CHECKS = {"django_alive.checks.check_database": {}}
ALIVE_CHECKS = getattr(settings, "ALIVE_CHECKS", DEFAULT_ALIVE_CHECKS)


def perform_healthchecks():
    # typing: () -> (bool, List[str])
    errors = []
    for func, kwargs in ALIVE_CHECKS.items():
        try:
            import_string(func)(**kwargs)
        except HealthcheckFailure as e:
            errors.append(str(e))
    return not errors, errors
