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

Unlike normal template tags, component template tags support special characters as keyword arguments. Specifically `_`, `-`, `@`, and `:`.

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

:::tip Changed in Slippers 0.5.0

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
