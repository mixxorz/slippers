from typing import Any, Dict

from django import template
from django.conf import settings
from django.template import Context
from django.template.base import Variable, token_kwargs

register = template.Library()


##
# Component tags
def create_component_tag(template_path):
    def do_component(parser, token):
        tag_name, *remaining_bits = token.split_contents()

        # Block components start with `#`
        # Expect a closing tag
        if tag_name[0] == "#":
            nodelist = parser.parse((f"/{tag_name[1:]}",))
            parser.delete_first_token()
        else:
            nodelist = None

        extra_context = token_kwargs(remaining_bits, parser)

        # Bits that are not keyword args are interpreted as `True` values
        boolean_args = [
            bit for bit in remaining_bits if bit not in extra_context.keys()
        ]

        # Allow component fragment to be assigned to a variable
        target_var = None
        if len(remaining_bits) >= 2 and remaining_bits[-2] == "as":
            target_var = remaining_bits[-1]

            # Strip "as variable" from being part of boolean args
            boolean_args = remaining_bits[:-2]

        extra_context.update({key: Variable("True") for key in boolean_args})

        return ComponentNode(nodelist, template_path, extra_context, target_var)

    return do_component


class ComponentNode(template.Node):
    def __init__(self, nodelist, template, extra_context, target_var=None):
        self.nodelist = nodelist
        self.template = template
        self.extra_context = extra_context
        self.target_var = target_var

    def render(self, context):
        children = self.nodelist.render(context) if self.nodelist else ""

        values = {
            key: value.resolve(context) for key, value in self.extra_context.items()
        }

        t = context.template.engine.get_template(self.template)
        output = t.render(
            Context({**values, "children": children}, autoescape=context.autoescape)
        )

        if self.target_var:
            context[self.target_var] = output
            return ""

        return output


def register_components(
    components: Dict[str, str], target_register: template.Library = None
) -> None:
    if target_register is None:
        target_register = register

    for tag_name, template_path in components.items():
        # Inline component
        target_register.tag(f"{tag_name}", create_component_tag(template_path))

        # Block component
        target_register.tag(f"#{tag_name}", create_component_tag(template_path))


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
    def __init__(self, var_map: Dict):
        self.var_map = var_map

    def render(self, context):
        context.update(
            {name: value.resolve(context) for name, value in self.var_map.items()}
        )
        return ""


@register.tag(name="var")
def do_var(parser, token):
    try:
        tag_name, var = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError(
            f"The syntax for {token.contents.split()[0]} is {{% var var_name=var_value %}}"
        )
    var_map = token_kwargs([var], parser)
    return VarNode(var_map)


##
# match filter
@register.filter(name="match")
def do_match(match_key, mapping):
    items = mapping.split(",")
    values_map = {}

    error_message = 'The syntax for match is {{ variable|match:"key1:value1,key2:value2,key3:value3" }}'

    for item in items:
        try:
            key, *value = item.split(":")

            key = key.strip()
            value = ":".join(value).strip()

            if not key or not value:
                raise template.TemplateSyntaxError(error_message)

            values_map[key] = value
        except ValueError:
            if settings.DEBUG:
                raise template.TemplateSyntaxError(error_message)
            continue

    return values_map.get(match_key, "")


##
# fragment tag
class FragmentNode(template.Node):
    def __init__(self, nodelist, target_var):
        self.nodelist = nodelist
        self.target_var = target_var

    def render(self, context):
        fragment = self.nodelist.render(context) if self.nodelist else ""
        context[self.target_var] = fragment
        return ""


@register.tag(name="fragment")
def do_fragment(parser, token):
    error_message = "The syntax for fragment is {% fragment as variable_name %}"

    try:
        tag_name, _, target_var = token.split_contents()

        nodelist = parser.parse(("endfragment",))
        parser.delete_first_token()
    except ValueError:
        if settings.DEBUG:
            raise template.TemplateSyntaxError(error_message)
        return ""

    return FragmentNode(nodelist, target_var)
