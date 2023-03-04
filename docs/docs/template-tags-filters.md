---
sidebar_position: 6
---

# Template tags and filters

Slippers includes a number of extra template tags and filters to help template authors build reusable components.

## attrs

The `attrs` tag is a handy shortcut that outputs template variables as element attributes.

```twig
{# input_field component #}
<input {% attrs type id name x-bind:class %}>

{# Usage #}
{% input_field type="text" id="first_name" name="first_name" x-bind:class="!isValid ? 'error': ''" %}

{# Output #}
<input type="text" id="first_name" name="first_name" x-bind:class="!isValid ? 'error': ''" />
```

The parameters passed to `attrs` are used as both the "key" of the attribute and the name of the variable to source its value from.

:::tip New in Slippers 0.5.0

Added support for special characters in keyword arguments.

:::

Boolean values are treated differently. `True` values become empty attributes, and `False` values aren't returned at all.

```twig
{# button component #}
<button {% attrs disabled %}>{{ children }}</button>

{# Usage #}
{% #button disabled=True %}Can't click me{% /button %}
{% #button disabled=False %}Click me{% /button %}

{# Output #}
<button disabled>Can't click me</button>
<button>Click me</button>
```

It's possible to specify the source of the attribute value by writing it as a keyword argument. This is useful if the attribute name is different from the variable you want to get it from.

```twig
{# input_field component #}
<input {% attrs type id=field_id name %}>

{# Usage #}
{% input_field type="text" field_id="first_name" name="first_name" %}

{# Output #}
<input type="text" id="first_name" name="first_name" />
```

It's possible to specify the default value of an attribute by declaring it with the [`var`](#var) tag

```twig
{# image component #}
{% var loading=loading|default:"lazy" %}
<img {% attrs src loading alt %}>

{# Usage #}
{% image src="..." alt="..." %}

{# Output #}
<img src="..." alt="..." loading="lazy" />
```

## fragment

The `fragment` tag allows template fragments to be assigned to variables.

```twig
{% fragment as my_fragment %}
  <p>Hello, World!</p>
{% endfragment %}

{# Output the HTML #}
{{ my_fragment }}

{# Pass it around #}
{% my_component content=my_fragment %}
{% include "my_app/my_other_component.html" with content=my_fragment %}
```

One handy use for `fragment` is string interpolation using DTL.

```twig
{% fragment as title %}
{{ items|floatformat:2 }} items found.
{% endfragment %}

{% list_item title=title %}
```

:::note

`fragment` can't be used inside of a `with` block.

:::

## match

The `match` filter outputs a string whose key matches the variable's value.

```twig
{% with first="outline" second="ghost" third="square" %}
  <button class="{{ first|match:"outline:btn-outline,ghost:btn-ghost" }}">Click me</button>
  <button class="{{ second|match:"outline:btn-outline,ghost:btn-ghost" }}">Click me</button>
  <button class="{{ third|match:"outline:btn-outline,ghost:btn-ghost" }}">Click me</button>
{% endwith %}

{# Output #}
<button class="btn-outline">Click me</button>
<button class="btn-ghost">Click me</button>
<button class="">Click me</button>
```

The syntax is:

```twig
{{ variable|match:"key1:value1,key2:value2,key3:value3" }}
```

Tip: You can use the `default` filter to set a default value if there are no matches.

```twig
{% with my_variable="nomatch" %}
  <button class="{{ my_variable|match:"outline:btn-outline,ghost:btn-ghost"|default:"btn" }}">Click me</button>
{% endwith %}

{# Output #}
<button class="btn">Click me</button>
```

## var

The `var` tag allows for assigning values to variables.

```twig
{% var foo="Hello, World!" %}

<div>{{ foo }}</div>

{# Output #}
<div>Hello, World!</div>
```

The `var` tag is intended to be used inside component templates as a means to document the variables it requires and specify defaults.

```twig title="button.html"
{% var variant=variant|default:"outline" %}

<button class="{{ variant|match:"outline:btn-outline,ghost:btn-ghost" }}">{{ children }}</button>
```

:::note

`var` can't be used inside of a `with` block.

:::

:::note

The `var` tag can be used outside a component's context, however, it is not recommended since it would pollute the global context.

:::
