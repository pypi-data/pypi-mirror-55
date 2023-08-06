import json
from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.core.fields import StreamField
from wagtail.core.models import Site
from .utils import date_handler
from .defaults import WAGTAIL_NAV_MENU_CHOICES_DEFAULT
from .nav_category_block import NavCategoryBlock
from .nav_content import nav_content


def site_default():
    return Site.objects.filter(is_default_site=True).first()


NAV_MENU_CHOICES = getattr(
    settings,
    'WAGTAIL_NAV_MENU_CHOICES',
    WAGTAIL_NAV_MENU_CHOICES_DEFAULT
)


class AbstractNavMenu(models.Model):
    site = models.ForeignKey(
        'wagtailcore.Site',
        db_index=True,
        on_delete=models.CASCADE,
        default=site_default
    )
    name = models.CharField(
        max_length=50,
        choices=NAV_MENU_CHOICES,
    )
    menu = StreamField([
        ('nav_category', NavCategoryBlock()),
    ] + nav_content)

    panels = [
        FieldPanel('site'),
        FieldPanel('name'),
        StreamFieldPanel('menu'),
    ]

    class Meta:
        # Translators: Model Name (singular)
        verbose_name = _('Navigation Menu')
        # Translators: Model Name (plural)
        verbose_name_plural = _('Navigation Menus')
        unique_together = ('site', 'name',)
        abstract = True

    def __str__(self):
        return self.name

    def stream_field_to_json(self, stream_field):
        """ Recursive function to turn the menu stream field into json """
        row = {}
        row['type'] = stream_field.block_type
        if hasattr(stream_field.block, 'get_serializable_data'):
            row['value'] = stream_field.block.get_serializable_data(
                stream_field.value)
        else:
            row['value'] = stream_field.value
        if row['type'] == "image" and row['value']:
            image = row['value']
            row['value'] = {
                "id": image.pk,
                "title": image.title,
                "url": image.file.url,
            }
        elif row['type'] == "nav_category":
            sub_nav = []
            for sub_stream_field in stream_field.value['sub_nav']:
                sub_nav.append(self.stream_field_to_json(sub_stream_field))
            row['value']['sub_nav'] = sub_nav
        return row

    def to_json(self):
        """ JSON representation of menu stream field """
        result = []
        for stream_field in self.menu:
            result.append(self.stream_field_to_json(stream_field))
        return json.dumps(result, default=date_handler)
