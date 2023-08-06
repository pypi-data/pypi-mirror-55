from django.utils.translation import gettext_lazy as _
from wagtail.core import blocks
from .nav_content import nav_content


class NavCategoryBlock(blocks.StructBlock):
    title = blocks.CharBlock()
    sub_nav = blocks.StreamBlock(nav_content)

    class Meta:
        icon = 'list-ul'
        template = 'nav_menus/nav_category.html'
        # Translators: Content Block Name
        verbose_name = _('Navigation Menu Category Block')
