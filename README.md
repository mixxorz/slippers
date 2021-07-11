# Slippers

Slippers is a library for Django that generates template tags for your HTML components.

```django
{% card variant="small" %}
  <h1>Slippers is cool</h1>
  {% button text="Super cool" %}
  {% button text="Lit af" variant="secondary" %}
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
    {{ children }}
  </div>
</div>
```

Next, create a `components.yml` file. By default, Slippers looks for this file in the root template folder.

```yaml
# myapp/templates/components.yml
# Components that can have children
block_components:
  card:
    # Template name as if you were using {% include %}
    template: "myapp/card.html"
 
# Components that don't have child elements
inline_components: 
  avatar:
    template: "myapp/avatar.html"
```

You can now use the components like so:

```django
{% load components %}

{% card heading="Slippers is awesome" %}
  <span>Hello {{ request.user.full_name }}!</span>

  <div>
    This is what you look like {% avatar user=request.user %}
  </div>
{% endcard %}
```

## Installation

```
pip install slippers
```

Add it to your `INSTALLED_APPS`:

```
INSTALLED_APPS = [
    ...
    'slippers',
    ...
]
```

## License

MIT
