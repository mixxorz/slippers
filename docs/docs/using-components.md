---
sidebar_position: 5
---

# Using components

## Block and inline component syntax

Components can be used in two ways: block-level or inline-level.

For example, given an `icon_button` component.

```django title="icon_button.html"
<button>{{ children }} {% icon name=icon %}</button>
```

We can use the block syntax to pass the label of the button as `children.`

```django
{% #icon_button icon="star" %}Favorite{% /icon_button %}
```

Note that `#` denotes the opening tag and `/` denotes the closing tag.

```html title="Output"
<button>Favorite <svg>...</svg></button>
```

If we didn't need to pass a label, or if the component itself doesn't use `{{ children }}`, we can use the inline syntax instead.

```django
{% icon_button icon="heart" %}
```

The inline syntax just uses the plain component name. No `#` or `/`.

```html title="Output"
<button><svg>...</svg></button>
```

## Passing variables

Unlike the `include` tag, using component template tags **will not** pass the current context to the child component. Variables need to be passed in explicitly.

```django
{% #button variant="primary" size="large" %}Hello{% /button %}
```

This is a deliberate design decision to improve readability and reduce side-effects.

You can of course still use `{% include %}` if you find that functionality more convenient.

## Assigning output to a variable

Similar to a [`fragment`](/docs/template-tags-filters#fragment) tag, a component's output can be assigned to a variable.

```django
{% #heading variant="large" as my_heading %}Hello, World{% /heading %}

{# Render it like a normal variable #}
{{ my_heading }}

{# Or pass to to another component #}
{% card_heading heading=my_heading %}
```
