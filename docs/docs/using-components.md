---
sidebar_position: 5
---

# Using components

## Block and inline component syntax

Components can be used in two ways: block-level or inline-level.

For example, given an `icon_button` component.

```twig title="icon_button.html"
<button>{{ children }} {% icon name=icon %}</button>
```

We can use the block syntax to pass the label of the button as `children.`

```twig
{% #icon_button icon="star" %}Favorite{% /icon_button %}
```

Note that `#` denotes the opening tag and `/` denotes the closing tag.

```html title="Output"
<button>Favorite <svg>...</svg></button>
```

If we didn't need to pass a label, or if the component itself doesn't use `{{ children }}`, we can use the inline syntax instead.

```twig
{% icon_button icon="heart" %}
```

The inline syntax just uses the plain component name. No `#` or `/`.

```html title="Output"
<button><svg>...</svg></button>
```

## Component context

Unlike the `include` tag, component template tags **do not** pass the current context to the child component. Variables need to be passed in explicitly.

```twig
{% #button variant="primary" size="large" %}Hello{% /button %}
```

In addition, any variable set inside of a component template does not leak out to to the global context.

```twig button.html
{% var class=class|default:"btn btn-primary" %}
<button {% attrs class %}>{{ children }}</button>

{# The `class` variable will not "leak" out onto the global context #}
```

This is a deliberate design decision to improve readability and reduce side-effects.

You can of course still use `{% include %}` if its behaviour is more convenient in specific circumstances.

## Keyword arguments

Unlike normal template tags, component template tags support special characters in keyword arguments. Specifically `_`, `-`, `@`, and `:`.

This can be used in conjunction with the [`attrs`](/docs/template-tags-filters#attrs) tag.

```twig
{# button component #}
<button {% attrs aria-role x-bind:class @click %}>{{ children }}</button>

{# Usage #}
{% #button aria-role="button" x-bind:class="!open ? 'hidden': ''" @click="myHandler" %}Hello{% /button %}

{# Output #}
<button aria-role="button" x-bind:class="!open ? 'hidden': ''" @click="myHandler">Hello</button>
```

This makes keyword arguments work more like HTML attributes.

:::tip New in Slippers 0.5.0

Added support for special characters in keyword arguments.

:::

## Assigning output to a variable

Similar to a [`fragment`](/docs/template-tags-filters#fragment) tag, a component's output can be assigned to a variable.

```twig
{% #heading variant="large" as my_heading %}Hello, World{% /heading %}

{# Render it like a normal variable #}
{{ my_heading }}

{# Or pass to to another component #}
{% card_heading heading=my_heading %}
```

:::note

Assigning component output to a variable cannot be done inside a `with` block.

:::

## Define types and defaults with front matter

As [shown in Component context](#component-context) you can define
default values by using the `var` tag:

```twig title="button.html"
{% var class=class|default:"btn btn-primary" %}
<button {% attrs class %}>{{ children }}</button>
```

If the defaults are more complex structures, using the `default` filter may not be enough. In such case you would need to define a custom tag or a filter to generate the defaults.

Another limit of using the `var` tag is that it doesn't check for types.

In these cases, you can add a front matter with custom Python code to define the types and defaults of the component's props.

Front matter is a block of code at the beginning of the file, which starts and ends with lines with 3 dashes:

```twig
---
props.types = {
    'required_string': str,
    'optional_number': Optional[int],
    'default_number': int,
}
props.defaults = {
    'default_number': 10,
}

props['new_number'] = props['default_number'] * 2
---

The context contains:

Required string: {{ required_string }}
Optional number: {{ optional_number }}
Default number: {{ default_number }}
New number: {{ new_number }}
```

The code in the front matter is evaluated as a regular Python code.

It exposes the `props` variable (instance of `slippers.props.Props`),
which has 3 special features:

### 1. `props.types` - If defined, component props are checked against types in `props.types` and raise `PropError` on mismatch.

Using the previous example, if we set `required_string` to `int`,
or it was `None`, this would raise `PropError`.

Since the type for `optional_number` is `Optional`, we CAN set `optional_number` to `None`, but setting it to other type like `str` would raise `PropError`.

Although `default_number` is NOT `Optional`, we provided a default value, so we won't raise an error if we don't provide the value (or provide `None`).

However, if the default value of `default_number` was NOT `int` this would raise `PropError`.

For convenience with defining the types, the front matter is already prepopulated with the `typing` module, effectively the same as calling:

```py
from typing import *
```

### 2. `props.defaults` - If defined, variables will fall back to these defaults if `None`.

So the button example from [Component context](#component-context) can be rewritten as:

```twig title="button.html"
---
props.defaults = {
    'class': 'btn btn-primary'
}
---
<button {% attrs class %}>{{ children }}</button>
```

And used as:

```twig
{# Usage #}
{% button %}
{# Output #}
<button class="btn btn-primary"></button>

{# Usage #}
{% button class="btn btn-secondary" %}
{# Output #}
<button class="btn btn-secondary"></button>
```

### 3. Props mapping - Add or modify props with `props['prop_name']`

To assign variables to the component's context, simply use:
```python
props['var_name'] = my_value
```

See the [next section](#preprocess-and-extend-component-context-with-front-matter)
which delves deeper into this.

## Preprocess and extend component context with front matter

Sometimes, you may want to define some data internal to the component,
like a static set of items in a menu.

Normally, you'd have to define the items one by one:

```twig title="menu.html"
<div class="menu">
  <h3>Menu</h3>
  <div class="menu-item">
    <a href="/path1">Link 1</a>
    <a href="/path2">Link 2</a>
    <a href="/path3">Link 3</a>
  </div>
</div>
```

Or pass them as props:

```twig title="menu.html"
<div class="menu">
  <h3>Menu</h3>
  <div class="menu-item">
    {% for name, href in items %}
    <a href="{{href}}">{{ name }}</a>
    {% endfor %}
  </div>
</div>
```

However, if these variables are never meant to be changed, then providing them through the props
doesn't make sense, as they will always be the same.

It would clutter the component's interface, and make a room for error, as you now have to make sure
to pass in all "static" variables every time you use the component:

```twig
{# You have to provide `items` every single time #}
{% menu items=items %}
{% menu items=items class="my_class" %}
```

Instead, you can make use of the front matter again, this time to
preprocess, define, or even import variables:

```twig title="menu.html"
---
from my_app.constants.icons import icon_bars_3

props.types = {
    'title_level': Optional[int],
}
props.defaults = {
    'title_level': 3,
}

props['items'] = [
  ('Link 1', '/path1'),
  ('Link 2', '/path2'),
  ('Link 3', '/path3')
]

props['title_tag'] = f'h{props['title_level']}'
---
<div class="menu">
  {{icon_bars_3}}
  <{{title_tag}}>Menu</{{title_tag}}>
  <div class="menu-item">
    {% for name, href in items %}
    <a href="{{href}}">{{ name }}</a>
    {% endfor %}
  </div>
</div>
```

Which can be used as:
```twig
{# Usage #}
{% menu title_tag=5 %}

{# Output #}
<div class="menu">
  <svg>
    <path><!-- ... --></path>
  </svg>
  <h5>Menu</h5>
  <div class="menu-item">
    <a href="/path1">Link 1</a>
    <a href="/path2">Link 2</a>
    <a href="/path3">Link 3</a>
  </div>
</div>
```

To assign variables to the component's context, simply use:
```python
props['var_name'] = my_value
```

And since the code in the front matter is evaluated as a regular Python code, we can import other modules.
