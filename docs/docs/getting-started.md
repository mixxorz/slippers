# Getting started

## What is Slippers?

The Django Template Language is awesome. It's fast, rich in features, and overall pretty great to work with.

Slippers aims to be augment DJT, adding just enough functionality to make building interfaces just that bit more _comfortable_.

It includes additional template tags and filters, but its headline feature is **reusable components**. Let's see how it works.

## Installation

You can get Slippers from PyPI.

```
pip install slippers
```

Next, add it to your project's `INSTALLED_APPS`.

```python title="settings.py"
INSTALLED_APPS = [
    ...,
    'slippers',
    ...,
]
```

Optionally, if you wanted Slippers to be available in all your templates without having to add `{% load slippers %}` manually, you can add `slippers.templatetags.slippers` as a built-in in your template settings.

```python {14}
# Example configuration
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
            "builtins": ["slippers.templatetags.slippers"],
        },
    },
]
```

If you don't add Slippers as a built-in, you will need to load `slippers` in your templates when you want to use it.

## Creating our first component

Let's create a card component that accepts a `heading` parameter and child elements.

```django title="myapp/templates/myapp/card.html"
<div class="card">
  <h1 class="card__header">{{ heading }}</h1>
  <div class="card__body">
    {{ children }}
  </div>
</div>
```

This is pretty much just a normal Django template; one that you would use in an `include` tag. One big difference is `{{ children }}`. This is where any child elements are rendered when this component is used.

The next step is to register our component. The easiest way to do this is to create a `components.yaml` file. This file should live in the root template folder. It tells Slippers which templates to register as components. It also serves as a handy directory for all components available in your app.

```yaml title="myapp/templates/components.yaml"
components:
  card: "myapp/card.html"
```

The name of the component in `components.yaml` becomes the template tag for that component. In this case, we're telling Slippers to register the `myapp/card.html` template as the `card` component.

And here's how to use it:

```django
{% load slippers %}

{% #card heading="I am the heading" %}
  <span>Hello {{ name|title }}!</span>
{% /card %}
```

Notice that we use `#` to denote the opening tag of a component and `/` to denote the closing tag. Anything within the opening and closing tags will be rendered as `{{ children }}`.

And here's the output:

```html
<div class="card">
  <h1 class="card__header">I am the heading</h1>
  <div class="card__body">
    <span>Hello Ryland Grace!</span>
  </div>
</div>
```

## Block vs Inline components

A component can be both block-level and inline-level. To show an example, let's create an `icon_button` component.

```django title="icon_button.html"
<button>{{ children }} {% icon name=icon %}</button>
```

If we wanted to display an `icon_button` with a label, we can use the block syntax.

```django
{% #icon_button icon="star" %}Favorite{% /icon_button %}
```

```html title="Output"
<button>Favorite <svg>...</svg></button>
```

If we wanted to display a button with just an icon in it, then we can use the inline syntax.

```django
{% icon_button icon="heart" %}
```

```html title="Output"
<button><svg>...</svg></button>
```
