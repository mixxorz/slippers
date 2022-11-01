from dataclasses import dataclass
from typing import Any, Dict, List, Literal, Optional

from django.utils.safestring import mark_safe

from rich.console import Console
from rich.panel import Panel
from typeguard import check_type, get_type_name

console = Console()


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


def check_prop_types(*, prop_types: PropTypes, props: Dict[str, Any]):
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
    "invalid": "Invalid prop '{name}' set on {component}. Expected {expected}, got {actual}.",
    "missing": "Required prop '{name}' of type {expected} not set on {component}.",
    "extra": "Extra prop '{name}' of type '{actual}' set on {component}.",
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
