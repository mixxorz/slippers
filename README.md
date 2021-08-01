[![Slippers](./docs/static/img/slippers.svg)](https://github.com/mixxorz/slippers)

---

[![PyPI version](https://badge.fury.io/py/slippers.svg)](https://badge.fury.io/py/slippers)
[![PyPI Supported Python Versions](https://img.shields.io/pypi/pyversions/slippers.svg)](https://pypi.python.org/pypi/slippers/)
[![PyPI Supported Django Versions](https://img.shields.io/pypi/djversions/slippers.svg)](https://docs.djangoproject.com/en/dev/releases/)
[![GitHub Actions (Code quality and tests)](https://github.com/mixxorz/slippers/workflows/Code%20quality%20and%20tests/badge.svg)](https://github.com/mixxorz/slippers)

Build reusable components in Django without writing a single line of Python.

```django
{% #quote %}
  {% quote_photo src="/django.jpg" %}

  {% #quote_text %}
    The Django template system recognizes that templates are most often written
    by designers, not programmers, and therefore should not assume Python
    knowledge.
  {% /quote_text %}

  {% #quote_attribution %}
    Design philosophies – Django
  {% /quote_attribution %}
{% /quote %}
```

## Why?

The Django Template Language is awesome. It's fast, rich in features, and overall pretty great to work with.

Slippers aims to be a superset of the Django Template Language, adding just enough functionality to make building interfaces just that bit more _comfortable_.

Its headline feature is **reusable components**.

## Show me how it works

Let's create a card component that accepts a `heading` parameter and child elements.

```django
{# myapp/templates/myapp/card.html #}
<div class="card">
  <h1 class="card__header">{{ heading }}</h1>
  <div class="card__body">
    {# Child elements are rendered by `{{ children }}` #}
    {{ children }}
  </div>
</div>
```

Next, we'll create a `components.yaml` file in the root template folder. This file tells slippers which templates to register as components. As a bonus, it serves as a useful index for all available components.

```yaml
# myapp/templates/components.yaml
components:
  card: "myapp/card.html"
```

The name of the component in `components.yaml` becomes the template tag for that component.

```django
{% load slippers %}

{% #card heading="Slippers is awesome" %}
  <span>Hello {{ request.user.full_name }}!</span>
{% /card %}
```

Notice that we use `#` to denote the start of a component block and `/` to denote the end.

And the output:

```html
<div class="card">
  <h1 class="card__header">Slippers is awesome</h1>
  <div class="card__body">
    <span>Hello Ryland Grace!</span>
  </div>
</div>
```

## Installation

```
pip install slippers
```

Add it to your `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    ...
    'slippers',
    ...
]
```

## Documentation

### The `components.yaml` file

This file should be placed at the root template directory. E.g. `myapp/templates/components.yaml`.

The structure of the file is as follows:

```yaml
components:
  # The key determines the name of the template tag. So `card` would generate
  # `{% #card %}{% /card %}`
  # The value is the path to the template file as it would be if used with {% include %}
  avatar: "myapp/avatar.html"
  card: "myapp/card.html"
```

### Context

Unlike `{% include %}`, using the component template tag **will not** pass the current context to the child component. This is a deliberate design decision. Components should be self-sufficient and not reliant on external state. If you find you need something from the parent context, you have to explicitly pass it in via keyword arguments. You can of course still use `{% include %}` as an alternative.

### Additional tags and filters

In addition to generating template tags for your components, Slippers also includes template tags and filters that make building reusable components easier.

#### `attrs` tag

The `attrs` tag is a handy shortcut that outputs template variables as element attributes.

```django
{# Usage #}
{% with foo="one" bar="two" baz="three" %}
  {% attrs foo bar baz %}
{% endwith %}

{# Output #}
foo="one" bar="two" baz="three"
```

The parameters passed to `attrs` are used for both the "key" of the attribute and the name of variable to source its value from.

Another example:

```django
{# Component #}
<input {% attrs type id name %}>

{# Usage #}
{% input_field type="text" id="first_name" name="first_name" %}

{# Output #}
<input type="text" id="first_name" name="first_name" />
```

True values become empty attributes, and false values aren't returned at all.

```django
{# Component #}
<button {% attrs disabled %}>{{ children }}</button>

{# Usage #}
{% #button disabled=True %}Can't click me{% /button %}
{% #button disabled=False %}Click me{% /button %}

{# Output #}
<button disabled>Can't click me</button>
<button>Click me</button>
```

It's possible to specify the source of the attribute value by writing it as a keyword argument. This is useful if the attribute name is different from the variable you want to get it from.

```django
{# Component #}
<input {% attrs type id=field_id name %}>

{# Usage #}
{% input_field type="text" field_id="first_name" name="first_name" %}

{# Output #}
<input type="text" id="first_name" name="first_name" />
```

## License

MIT
