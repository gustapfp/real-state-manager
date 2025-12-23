import contextlib

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class LocationsConfig(AppConfig):
    name = "real_state_manager.locations"
    verbose_name = _("Locations")

    def ready(self):
        with contextlib.suppress(ImportError):
            import real_state_manager.locations.signals  # noqa: F401, PLC0415  # pyright: ignore[reportMissingImports]
