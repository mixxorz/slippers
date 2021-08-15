---
sidebar_position: 3
---

# Getting started

Before we start, first make sure to [install slippers](/docs/installation/).

## Creating our first component

Let's create a card component that accepts a `heading` parameter and child elements.

```twig title="myapp/templates/myapp/card.html"
<div class="card">
  <h1 class="card__header">{{ heading }}</h1>
  <div class="card__body">
    {{ children }}
  </div>
</div>
```

This is just a normal Django template; not too dissimilar from one that you would use with an `include` tag. Something you may have noticed is `{{ children }}`. This is where any child elements are rendered when this component is used.

Before we can use our new component, we need to register it. The easiest way to do this is to create a `components.yaml` file. This file should live in the root template folder. It tells Slippers which templates to register as components. It also serves as a handy directory for all components available in your app.

```yaml title="myapp/templates/components.yaml"
components:
  card: "myapp/card.html"
```

The name of the component in `components.yaml` becomes the template tag for that component. In this case, we're registering the `myapp/card.html` template as the `card` component.

Now we can use our new `card` component.

```twig
{% load slippers %}

{% #card heading="I am the heading" %}
  <span>Hello {{ name|title }}!</span>
{% /card %}
```

Notice that we use `#` to denote the opening tag of a component and `/` to denote the closing tag. Anything within the opening and closing tags is passed to the component as `children`.

And here's the output:

```html
<div class="card">
  <h1 class="card__header">I am the heading</h1>
  <div class="card__body">
    <span>Hello Ryland Grace!</span>
  </div>
</div>
```

Tada :tada:
