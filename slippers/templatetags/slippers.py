from typing import Any, Dict

from django import template
from django.template import Context
from django.template.base import FilterExpression, token_kwargs

register = template.Library()


##
# Inline components
def do_inline_component(**kwargs):
    return kwargs


def register_inline_components(components: Dict[str, str]) -> None:
    for tag_name, template_path in components.items():
        # Inline components use Django's built-in `inclusion_tag`
        register.inclusion_tag(name=tag_name, filename=template_path)(
            do_inline_component
        )


##
# Block components
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

        values = {
            key: value.resolve(context) for key, value in self.extra_context.items()
        }

        return t.render(
            Context({**values, "children": children}, autoescape=context.autoescape)
        )


def register_block_components(components: Dict[str, str]) -> None:
    for tag_name, template_path in components.items():
        register.tag(tag_name, create_block_component_tag(template_path))


##
# attr tag
def attr_string(key: str, value: Any):
    if isinstance(value, bool):
        return key if value else ""

    return f'{key}="{value}"'


class AttrsNode(template.Node):
    def __init__(self, attr_map: Dict):
        self.attr_map = attr_map

    def render(self, context):
        values = {key: value.resolve(context) for key, value in self.attr_map.items()}
        attr_strings = [
            attr_string(key, value) for key, value in values.items() if value
        ]
        return " ".join(attr_strings)


@register.tag(name="attrs")
def do_attrs(parser, token):
    tag_name, *attrs = token.split_contents()

    # Format all tokens to be attr=attr so we can use token_kwargs() on it
    all_attrs = [attr if "=" in attr else f"{attr}={attr}" for attr in attrs]
    attr_map = token_kwargs(all_attrs, parser)
    return AttrsNode(attr_map)


##
# var tag
class VarNode(template.Node):
    def __init__(self, var_name: FilterExpression, value: FilterExpression):
        self.var_name = var_name
        self.value = value

    def render(self, context):
        var_name = self.var_name.resolve(context)
        value = self.value.resolve(context)
        context[var_name] = value
        return ""


@register.tag(name="var")
def do_var(parser, token):
    try:
        tag_name, var_name, value = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError(
            f'The syntax for {token.contents.split()[0]} is {{% var "var_name" var_value %}}'
        )
    return VarNode(parser.compile_filter(var_name), parser.compile_filter(value))
