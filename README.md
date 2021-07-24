[![Slippers](https://user-images.githubusercontent.com/3102758/125623857-02364192-ad2d-4a45-8106-376817a92d3f.png)](https://github.com/mixxorz/slippers)

---

[![PyPI version](https://badge.fury.io/py/slippers.svg)](https://badge.fury.io/py/slippers)
[![PyPI Supported Python Versions](https://img.shields.io/pypi/pyversions/slippers.svg)](https://pypi.python.org/pypi/slippers/)
[![PyPI Supported Django Versions](https://img.shields.io/pypi/djversions/slippers.svg)](https://docs.djangoproject.com/en/dev/releases/)
[![GitHub Actions (Code quality and tests)](https://github.com/mixxorz/slippers/workflows/Code%20quality%20and%20tests/badge.svg)](https://github.com/mixxorz/slippers)

Slippers allows you to build reusable components in Django without writing a single line of Python.

```django
{% card variant="small" %}
  <h1>Slippers is cool</h1>

  {% button %}Super cool{% endbutton %}
  {% button variant="secondary" %}Lit af{% endbutton %}
{% endcard %}
```

## Why?

I want to be able to make reusable components, but the syntax for `{% include %}` is too verbose. Plus it doesn't allow me to specify child elements.

## Show me how it works

First create your template. Wherever you would normally put it is fine.

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

Next, create a `components.yaml` file. By default, Slippers looks for this file in the root template folder.

```yaml
# myapp/templates/components.yaml
# Components that have child elements
block_components:
  card: "myapp/card.html"

# Components that don't have child elements
inline_components:
  avatar: "myapp/avatar.html"
```

You can now use the components like so:

```django
{% load slippers %}

{% card heading="Slippers is awesome" %}
  <span>Hello {{ request.user.full_name }}!</span>
{% endcard %}
```

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
# Components that have child elements are called "block" components
block_components:
  # The key determines the name of the template tag. So `card` would generate
  # `{% card %}{% endcard %}`
  # The value is the path to the template file as it would be if used with {% include %}
  card: "myapp/card.html"

# Components that don't have child elements are called "inline" components
inline_components:
  avatar: "myapp/avatar.html"
```

This file also doubles as an index of available components which is handy.

### Context

Unlike `{% include %}`, using the component template tag **will not** pass the
current context to the child component. This is a design decision. If you need
something from the parent context, you have to explicitly pass it in via keyword
arguments, or use `{% include %}` instead.

```django
{% with not_passed_in="Lorem ipsum" %}
  {% button is_passed_in="Dolor amet" %}Hello{% endbutton %}
{% endwith %}
```

### Additional tags and filters

In addition to generating template tags for your components, Slippers also includes template tags and filters that make building reusable components easier.

#### `attrs` tag

The `attrs` tag allows you to "forward" attributes to your components.

```django
{# Component #}
<input {% attrs type id name %}>

{# Usage #}
{% input_field type="text" id="first_name" name="first_name" %}

{# Output #}
<input type="text" id="first_name" name="first_name" />
```

**Boolean values**

True values become empty attributes, and false values aren't returned at all.

```django
{# Component #}
<button {% attrs disabled %}>{{ children }}</button>

{# Usage #}
{% button disabled=True %}Can't click me{% endbutton %}
{% button disabled=False %}Click me{% endbutton %}

{# Output #}
<button disabled>Can't click me</button>
<button>Click me</button>
```

**Specify source**

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
