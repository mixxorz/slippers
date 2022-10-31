from dataclasses import dataclass
from typing import Any, Dict, List, Literal, Optional
from warnings import warn

from django import template
from django.conf import settings
from django.template import Context
from django.utils.safestring import mark_safe

from rich.console import Console
from rich.panel import Panel
from typeguard import check_type, get_type_name

from slippers.template import slippers_token_kwargs

register = template.Library()
console = Console()


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

        extra_context = slippers_token_kwargs(all_bits, parser)

        # Allow component fragment to be assigned to a variable
        target_var = None
        if len(remaining_bits) >= 2 and remaining_bits[-2] == "as":
            target_var = remaining_bits[-1]

        return ComponentNode(
            tag_name=tag_name,
            nodelist=nodelist,
            template_path=template_path,
            extra_context=extra_context,
            origin_template_name=parser.origin.template_name,
            origin_lineno=token.lineno,
            target_var=target_var,
        )

    return do_component


class PropTypes:
    """Represents the PropTypes of a component"""

    def __init__(self, types: Dict[str, type], defaults: Dict[str, Any]):
        self.types = types
        self.defaults = defaults

    @classmethod
    def from_source_code(cls, source_code: str):
        """Parse a component's source code to extract PropTypes"""

        source_locals = {}

        # Execute the source code in a local scope
        exec(f"from typing import *\n{source_code}", {}, source_locals)

        # Variables with type hints are prop types
        types = source_locals.get("__annotations__", {})

        # Prop declarations with set values are prop defaults
        defaults = {
            key: source_locals[key] for key in types.keys() if key in source_locals
        }

        return cls(types, defaults)


@dataclass
class PropError:
    error: Literal["invalid", "missing", "extra"]
    name: str
    expected: Optional[type]
    actual: Optional[type]


def check_prop_types(
    *, prop_types: PropTypes, props: Dict[str, Any], tag_name, template_name
):
    """Check that props are of the correct type"""

    errors = []

    # Check for missing props
    for name, expected in prop_types.types.items():
        if name not in props:
            if name in prop_types.defaults:
                # Prop is missing but has a default value
                continue
            else:
                # Prop is missing and has no default value
                errors.append(
                    PropError(
                        error="missing",
                        name=name,
                        expected=expected,
                        actual=None,
                    )
                )

    # Check for invalid props
    for name, actual in props.items():
        if name in prop_types.types:
            expected = prop_types.types[name]
            try:
                check_type(name, actual, expected)
            except TypeError:
                errors.append(
                    PropError(
                        error="invalid",
                        name=name,
                        expected=expected,
                        actual=type(actual),
                    )
                )

    # Check for extra props
    for name, actual in props.items():
        if name not in prop_types.types:
            errors.append(
                PropError(
                    error="extra",
                    name=name,
                    expected=None,
                    actual=type(actual),
                )
            )

    return errors


error_message_templates = {
    "invalid": "Invalid prop '{name}' passed to '{component}'. Expected {expected}, got {actual}.",
    "missing": "Required prop '{name}' of type {expected} not passed to '{component}'.",
    "extra": "Extra prop '{name}' of type '{actual}' passed to '{component}'.",
}


def print_errors(
    *, errors: List[PropError], tag_name: str, template_name: str, lineno: int
):
    """Print errors to the console"""

    error_messages = [
        error_message_templates[error.error].format(
            name=error.name,
            component=tag_name,
            expected=get_type_name(error.expected),
            actual=get_type_name(error.actual),
        )
        for error in errors
    ]

    console.print(
        Panel(
            "\n".join(error_messages),
            style="yellow",
            expand=False,
            title=(
                r"\[slippers] "
                f"Failed prop types: {tag_name} at "
                f"{template_name}:{lineno}"
            ),
            title_align="left",
        )
    )


def render_error_html(
    *, errors: List[PropError], tag_name: str, template_name: str, lineno: int
):
    """Output errors to the browser console"""

    error_messages = [
        error_message_templates[error.error].format(
            name=error.name,
            component=tag_name,
            expected=get_type_name(error.expected),
            actual=get_type_name(error.actual),
        )
        for error in errors
    ]

    error_message = (
        f"[slippers] Failed prop types: {tag_name} at {template_name}:{lineno}\\n  "
    )

    error_message += "\\n  ".join(error_messages)

    return mark_safe(f"""<script>console.error("{error_message}")</script>""")


class ComponentNode(template.Node):
    def __init__(
        self,
        tag_name,
        nodelist,
        template_path,
        extra_context,
        origin_template_name,
        origin_lineno,
        target_var=None,
    ):
        self.tag_name = tag_name
        self.nodelist = nodelist
        self.template_path = template_path
        self.extra_context = extra_context
        self.origin_template_name = origin_template_name
        self.origin_lineno = origin_lineno
        self.target_var = target_var

    def render(self, context):
        children = self.nodelist.render(context) if self.nodelist else ""

        values = {
            key: value.resolve(context) for key, value in self.extra_context.items()
        }

        template = context.template.engine.get_template(self.template_path)

        raw_output = template.render(
            Context({**values, "children": children}, autoescape=context.autoescape)
        )

        # Find front matter
        # Front matter is used for runtime type checking
        source_parts = template.source.split("---", 2)

        # If there is front matter...
        if len(source_parts) == 3:
            prop_types = PropTypes.from_source_code(source_parts[1])

            errors = check_prop_types(
                prop_types=prop_types,
                props=values,
                tag_name=self.tag_name,
                template_name=self.origin_template_name,
            )
            # Strip front matter from output
            content = raw_output.split("---", 2)[2]

            if errors:
                print_errors(
                    errors=errors,
                    tag_name=self.tag_name,
                    template_name=self.origin_template_name,
                    lineno=self.origin_lineno,
                )

                content = content + render_error_html(
                    errors=errors,
                    tag_name=self.tag_name,
                    template_name=self.origin_template_name,
                    lineno=self.origin_lineno,
                )

            output = mark_safe(content)
        else:
            # No front matter, no type checking
            output = raw_output

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
