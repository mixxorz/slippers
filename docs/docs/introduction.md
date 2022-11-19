---
sidebar_position: 2
---

# Examples

### Hello World

A very simple component that doesn't use `children`. It can be used like a
normal template tag.

```twig title='Greeting: "greeting.html"'
<h1>Hello, {{ name }}!</h1>
```

```twig title="Template"
{% Greeting name="World" %}
```

```html title="Output"
<h1>Hello, World!</h1>
```

### Children

You can use the `children` prop to access the rendered template fragment passed
into the component block.

```twig title='Alert: "alert.html"'
<div class="alert alert--{{ severity }}">
  <p class="alert__message">{{ children }}</p>
</div>
```

```twig title="Template"
{% #Alert severity="error" %}This is an error message{% /Alert %}
```

The opening tag is the component name prefixed with a `#` and the closing tag is
the component name prefixed with a `/`. Other props can be passed in as usual.

```twig title="Output"
<div class="alert alert--error">
  <p class="alert__message">This is an error message</p>
</div>
```

### Front matter

Components can include Python front matter. Code in the front matter is executed
immediately before the component is rendered.

```twig title='Answer: "answer.html"'
---
props['answer'] = props['number'] * 42
---

<h1>{{ number }} times 42 is {{ answer }}</h1>
```

`props` is a special object that you can use to access the props passed to your
component. It can also be used to modify the props available in the template.

```twig title="Template"
{% Answer number=7 %}
```

```twig title="Output"
<h1>7 times 42 is 294</h1>
```

### Default values

Default values for your props can be specified using the `props.defaults`
dictionary.

```twig title='Button: "button.html"'
---
props.defaults = {
    'variant': 'primary',
}
---

<button class="button button-{{ variant }}">{{ children }}</button>
```

```twig title="Template"
{% #Button %}Primary button{% /Button %}
{% #Button variant="secondary" %}Secondary button{% /Button %}
```

```twig title="Output"
<button class="button button-primary">Primary button</button>
<button class="button button-secondary">Secondary button</button>
```

### Prop types

Slippers can also type check your props at runtime. By default this is only
enabled when `DEBUG` is `True`. The error messages will appear in your terminal
and browser console.

```twig title='Icon: "icon.html"'
---
props.types = {
    'name': Literal['error', 'warning'],
    'variant': Literal['light', 'dark'],
    'size': int,
}
props.defaults = {
    'variant': 'light',
    'size': 16,
}
---

<span class="icon icon--{{ variant }}">
  {% if name == 'checkmark' %}
  <svg width="{{ size }}" height="{{ size }}">...checkmark svg...</svg>
  {% elif name == 'cross' %}
  <svg width="{{ size }}" height="{{ size }}">...cross svg...</svg>
  {% endif %}
</span>
```

```twig title="Template"
{% Icon name="checkmark" %}
{% Icon name="cross" variant="dark" size=24 %}
```

```twig title="Output"
<span class="icon icon--light">
  <svg width="16" height="16">...checkmark svg...</svg>
</span>
<span class="icon icon--dark">
  <svg width="24" height="24">...cross svg...</svg>
</span>
```
