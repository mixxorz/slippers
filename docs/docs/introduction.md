# Introduction

The Django Template Language is awesome. It's fast, rich in features, and overall pretty great to work with.

Slippers aims to be a superset of the Django Template Language, adding just enough functionality to make building interfaces just that bit more _comfortable_.

Its headline feature is **reusable components**.

## Demo

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
