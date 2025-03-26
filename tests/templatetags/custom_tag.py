from django import template

from slippers.templatetags.slippers import create_component_tag

register = template.Library()
register.tag(
    "custom_component",
    create_component_tag("custom_register.html", closing_tag="endcustom_component"),
)
