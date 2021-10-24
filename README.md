[![Slippers](https://mitchel.me/slippers/img/slippers.svg)](https://github.com/mixxorz/slippers)

---

[![PyPI version](https://badge.fury.io/py/slippers.svg)](https://badge.fury.io/py/slippers)
[![PyPI Supported Python Versions](https://img.shields.io/pypi/pyversions/slippers.svg)](https://pypi.python.org/pypi/slippers/)
[![PyPI Supported Django Versions](https://img.shields.io/pypi/djversions/slippers.svg)](https://docs.djangoproject.com/en/dev/releases/)
[![GitHub Actions (Code quality and tests)](https://github.com/mixxorz/slippers/workflows/Code%20quality%20and%20tests/badge.svg)](https://github.com/mixxorz/slippers)

Build reusable components in Django without writing a single line of Python.

```django
{% #quote %}
  {% quote_photo src="/project-hail-mary.jpg" %}

  {% #quote_text %}
    “I penetrated the outer cell membrane with a nanosyringe."
    "You poked it with a stick?"
    "No!" I said. "Well. Yes. But it was a scientific poke
    with a very scientific stick.”
  {% /quote_text %}

  {% #quote_attribution %}
    Andy Weir, Project Hail Mary
  {% /quote_attribution %}
{% /quote %}
```

## What is Slippers?

The Django Template Language is awesome. It's fast, rich in features, and overall pretty great to work with.

Slippers aims to augment DTL, adding just enough functionality to make building interfaces just that bit more _comfortable_.

It includes additional template tags and filters, but its headline feature is **reusable components**.

```django
{% #button variant="primary" %}See how it works{% /button %}
```

[See how it works](https://mitchel.me/slippers/docs/getting-started/)

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

Full documentation can be found on the [Slippers documentation site](https://mitchel.me/slippers/).

## Contributors

[![Contributors](https://contrib.rocks/image?repo=mixxorz/slippers)](https://github.com/mixxorz/slippers/graphs/contributors)

## License

MIT
