import re
from typing import Any, Dict, Tuple
from warnings import warn

from django import template
from django.conf import settings as django_settings
from django.template import Context
from django.utils.safestring import mark_safe

from slippers.conf import settings
from slippers.props import Props, check_prop_types, print_errors, render_error_html
from slippers.template import slippers_token_kwargs

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

        # Bits that are not keyword args are interpreted as `True` values
        all_bits = [bit if "=" in bit else f"{bit}=True" for bit in remaining_bits]

        raw_attributes = slippers_token_kwargs(all_bits, parser)

        # Allow component fragment to be assigned to a variable
        target_var = None
        if len(remaining_bits) >= 2 and remaining_bits[-2] == "as":
            target_var = remaining_bits[-1]

        return ComponentNode(
            tag_name=tag_name,
            nodelist=nodelist,
            template_path=template_path,
            raw_attributes=raw_attributes,
            origin_template_name=parser.origin.template_name,
            origin_lineno=token.lineno,
            target_var=target_var,
        )

    return do_component


def extract_template_parts(code: str) -> Tuple[str, str]:
    """Extract the front matter and template sections from a component's code"""

    # Components that have front matter must start with `---`
    if not code.strip().startswith("---"):
        return "", code

    # Split the code into front matter and template
    parts = re.split(r"^---\s*$", code, maxsplit=2, flags=re.MULTILINE)

    # Content only
    if len(parts) == 1:
        return "", parts[0]

    # Front matter and content
    if len(parts) == 3:
        return parts[1].strip(), parts[2]  # Don't strip template

    # Any other case, just render the template as is
    return "", code


class ComponentNode(template.Node):
    def __init__(
        self,
        tag_name,
        nodelist,
        template_path,
        raw_attributes,
        origin_template_name,
        origin_lineno,
        target_var=None,
    ):
        self.tag_name = tag_name
        self.nodelist = nodelist
        self.template_path = template_path
        self.raw_attributes = raw_attributes
        self.origin_template_name = origin_template_name
        self.origin_lineno = origin_lineno
        self.target_var = target_var

    def render(self, context):
        children = self.nodelist.render(context) if self.nodelist else ""

        attributes = {
            key: value.resolve(context) for key, value in self.raw_attributes.items()
        }

        template = context.template.engine.get_template(self.template_path)

        source_front_matter = extract_template_parts(template.source)[0]

        prop_errors = None

        # Stage 1: Prop checking
        if source_front_matter:
            props = Props.from_string(attributes, source_front_matter)

            if settings.SLIPPERS_RUNTIME_TYPE_CHECKING:
                prop_errors = check_prop_types(
                    attributes=attributes,
                    types=props.types,
                    defaults=props.defaults,
                )

            if "shell" in settings.SLIPPERS_TYPE_CHECKING_OUTPUT and prop_errors:
                print_errors(
                    errors=prop_errors,
                    tag_name=self.tag_name,
                    template_name=self.origin_template_name,
                    lineno=self.origin_lineno,
                )

            # Load prop defaults into props
            attributes = {**props}

        # Stage 2: Render template
        raw_output = template.render(
            Context({**attributes, "children": children}, autoescape=context.autoescape)
        )

        output_template_section = mark_safe(extract_template_parts(raw_output)[1])

        if "browser_console" in settings.SLIPPERS_TYPE_CHECKING_OUTPUT and prop_errors:
            # Append prop errors to output
            output = output_template_section + render_error_html(  # type: ignore
                errors=prop_errors,
                tag_name=self.tag_name,
                template_name=self.origin_template_name,
                lineno=self.origin_lineno,
            )
        else:
            output = output_template_section

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

    # Replace `_` with `-`
    # an underscore is not a valid character in an HTML attribute name
    # a hyphen is not a valid character in a Django template variable name
    # So we can use an underscore when we want to use a hyphen in an HTML attribute name
    # e.g. `aria_role` turns into `aria-role`
    if "_" in key:
        warn(
            f"Underscores in attribute names are deprecated. Use hyphens instead. {key}",
            DeprecationWarning,
            stacklevel=2,
        )
    key = key.replace("_", "-")

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
    attr_map = slippers_token_kwargs(all_attrs, parser)
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
    error_message = (
        f"The syntax for {token.contents.split()[0]} is {{% var var_name=var_value %}}"
    )
    try:
        tag_name, var = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError(error_message)

    var_map = slippers_token_kwargs([var], parser)
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
            if django_settings.DEBUG:
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
        if django_settings.DEBUG:
            raise template.TemplateSyntaxError(error_message)
        return ""

    return FragmentNode(nodelist, target_var)


##
# slippers errors UI
@register.inclusion_tag("slippers/errors.html")
def slippers_errors():
    return
