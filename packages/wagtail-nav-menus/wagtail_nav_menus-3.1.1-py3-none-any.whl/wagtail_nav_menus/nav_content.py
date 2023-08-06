from django.conf import settings
from .defaults import WAGTAIL_NAV_MENU_TYPES_DEFAULT
from .loading import get_class


NAV_MENU_TYPES = getattr(
    settings,
    'WAGTAIL_NAV_MENU_TYPES',
    WAGTAIL_NAV_MENU_TYPES_DEFAULT
)

nav_content = []
for name, module_label, class_name in NAV_MENU_TYPES:
    nav_content.append(
        (name, get_class(module_label, class_name)()),
    )
