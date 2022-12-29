import json
import sys
from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Union

if sys.version_info >= (3, 8):
    from typing import Literal, get_args, get_origin
else:
    from typing_extensions import Literal, get_args, get_origin

from django.utils.html import SafeString
from django.utils.safestring import mark_safe

from rich.console import Console
from rich.panel import Panel
from typeguard import check_type, get_type_name

console = Console()


class Props(Mapping):
    """Props object used in component code"""

    def __init__(
        self,
        attributes: Dict[str, Any],
        types: Dict[str, type],
        defaults: Dict[str, Any],
    ):
        self._attributes = {**attributes}
        self.types = types
        self.defaults = defaults

    def __getitem__(self, key: str) -> Any:
        if key in self._attributes:
            return self._attributes[key]

        if key in self.defaults:
            return self.defaults[key]

        return None

    def __setitem__(self, key: str, value: Any) -> None:
        self._attributes[key] = value

    def __iter__(self):
        return iter({**self._attributes, **self.defaults})

    def __len__(self):
        return len({**self._attributes, **self.defaults})

    @classmethod
    def from_string(cls, attributes: Dict[str, Any], code: str) -> "Props":
        """Parse a component's code section to extract PropTypes and defaults"""

        props = cls(attributes, {}, {})

        code_locals = {"props": props}

        # Execute the source code in a local scope
        exec(f"from typing import *\n{code}", {}, code_locals)

        return props


@dataclass
class PropError:
    error: Literal["invalid", "missing", "extra"]
    name: str
    expected: Optional[type]
    actual: Optional[type]


def check_prop_types(
    *,
    attributes: Dict[str, Any],
    types: Dict[str, type],
    defaults: Dict[str, Any],
) -> List[PropError]:
    """Check that props are of the correct type"""

    errors = []

    # Check for missing props
    for name, expected in types.items():
        if name not in attributes:
            if get_origin(expected) is Union and type(None) in get_args(expected):
                # Props with Optional types are not required
                continue
            elif name in defaults:
                # Props with defaults are not required
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
    for name, actual in attributes.items():
        if name in types:
            expected = types[name]
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
    for name, actual in attributes.items():
        if name not in types:
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
    "invalid": "Invalid prop '{name}' set on '{component}'. Expected '{expected}', got '{actual}'.",
    "missing": "Required prop '{name}' of type '{expected}' not set on '{component}'.",
    "extra": "Extra prop '{name}' of type '{actual}' set on '{component}'.",
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
) -> SafeString:
    """Output errors to the browser console"""

    # Remove # from tag name
    tag_name = tag_name.lstrip("#")

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

    warnings_html = f'<script>console.error("{error_message}")</script>'

    # Output the error as JSON
    data = json.dumps(
        {
            "tag_name": tag_name,
            "template_name": template_name,
            "lineno": lineno,
            "errors": [
                {
                    "error": error.error,
                    "name": error.name,
                    "expected": get_type_name(error.expected),
                    "actual": get_type_name(error.actual),
                }
                for error in errors
            ],
        }
    )

    data_html = f"""
        <script>
            window.slippersPropErrors = window.slippersPropErrors || [];
            window.slippersPropErrors.push({data});
        </script>
    """

    return mark_safe(warnings_html + data_html)  # type: ignore
