---
sidebar_position: 1
---

# Getting started

Slippers is a UI component framework for Django. It extends Django’s template
language to provide better ergonomics around writing and using reusable UI
components.

## Install

```
pip install slippers
```

Add `slippers` to `INSTALLED_APPS` and `slippers.templatetags.slippers` to
`TEMPLATES['OPTIONS']['builtins']`.

```python title="settings.py" {3,19}
INSTALLED_APPS = [
    ...,
    'slippers',
    ...,
]

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

## Basic example

This is how you can create a `Button` component with Slippers.

```slippers title="Button.html"
<button class="button button--{{ variant }}">{{ children }}</button>
```

`children` is a special prop that contains the rendered template fragment passed
into the component block.

Next create a `components.yaml` file to register your component.

```yaml
components:
  Button: "Button.html"
```

The `components` object contains all of your registered components. The key is
what the component will be called and the value is the path to its template.

You can use the `Button` component like this:

```slippers
{% #Button variant="primary" %}Click me{% /Button %}
```

The opening tag is the component name prefixed with a `#` and the closing tag is
the component name prefixed with a `/`. Other props can be passed in as usual.

```html title="Output"
<button class="button button--primary">Click me</button>
```
