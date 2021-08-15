---
sidebar_position: 1
---

import Link from "@docusaurus/Link";

# Introduction

## What is Slippers?

The Django Template Language is awesome. It's fast, rich in features, and overall pretty great to work with.

Slippers aims to augment DTL, adding just enough functionality to make building interfaces just that bit more _comfortable_.

It includes additional template tags and filters, but its headline feature is **reusable components**.

```twig
{% #button variant="primary" %}See how it works{% /button %}
```

<Link className="button button--primary" to="/docs/getting-started">See how it works </Link>

## Motivation

On the projects I work on, we usually build the front-end using [Atomic Design](https://bradfrost.com/blog/post/atomic-web-design/) principles and [django-pattern-library](https://github.com/torchbox/django-pattern-library). Templates for buttons, icons, form fields, etc., are built and then included wherever they are needed.

```twig
{% url "project:add_data" as add_data_url %}
{% include "patterns/molecules/button/button.html" with label="Add data" href=add_data_url %}
```

As you can see, the syntax for this is quite verbose. You can just imagine how this would be like if we had a template that used many components.

What's more, we can't pass HTML down to these components with `{% include %}`.

```twig
<p>I want this to be my content.</p>

{# How do I pass the HTML to the component?? #}
{% include "patterns/molecules/card/card.html" %}
```

We can work around this by creating custom template tags. This, however, requires the developer to know Python, and specifically, how to create [advanced custom template tags](https://docs.djangoproject.com/en/3.2/howto/custom-template-tags/#advanced-custom-template-tags). This isn't something we can always assume.

In fact, Django's design philosophy states:

> The Django template system recognizes that templates are most often written by designers, not programmers, and therefore should not assume Python knowledge.

Moreover, the process of making reusable components by creating a custom template tag is also somewhat of a hassle.

The best code is no code as they say. And so, Slippers to the rescue.
