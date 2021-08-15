---
sidebar_position: 2
---

# Installation

You can get Slippers from PyPI.

```
$ pip install slippers

# Or if you're using poetry
$ poetry add slippers
```

Add `slippers` to `INSTALLED_APPS`

```python title="settings.py"
INSTALLED_APPS = [
    ...,
    'slippers',
    ...,
]
```

You're done. :tada:

---

Optionally, if you want Slippers to be available in all your templates without having to `{% load slippers %}` manually, you can add `slippers.templatetags.slippers` as a built-in in your template settings.

```python title="settings.py" {13}
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

If you choose not to add slippers as a built-in, you will need to add `{% load slippers %}` to the top of your template whenever you want to use Slippers components.
