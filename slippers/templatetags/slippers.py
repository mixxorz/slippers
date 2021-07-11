from typing import Dict

from django import template
from django.template import Context
from django.template.base import token_kwargs

register = template.Library()


def do_inline_component(**kwargs):
    return kwargs


def create_block_component_tag(template_path):
    def do_block_component(parser, token):
        tag_name, *remaining_bits = token.split_contents()
        extra_context = token_kwargs(remaining_bits, parser)
        nodelist = parser.parse((f"end{tag_name}",))
        parser.delete_first_token()
        return BlockComponentNode(nodelist, template_path, extra_context)

    return do_block_component


class BlockComponentNode(template.Node):
    def __init__(self, nodelist, template, extra_context):
        self.nodelist = nodelist
        self.template = template
        self.extra_context = extra_context

    def render(self, context):
        children = self.nodelist.render(context)
        t = context.template.engine.get_template(self.template)

        values = {key: val.resolve(context) for key, val in self.extra_context.items()}

        return t.render(
            Context({**values, "children": children}, autoescape=context.autoescape)
        )


def register_inline_components(components: Dict[str, str]) -> None:
    for tag_name, template_path in components.items():
        # Inline components use Django's built-in `inclusion_tag`
        register.inclusion_tag(name=tag_name, filename=template_path)(
            do_inline_component
        )


def register_block_components(components: Dict[str, str]) -> None:
    for tag_name, template_path in components.items():
        register.tag(tag_name, create_block_component_tag(template_path))
