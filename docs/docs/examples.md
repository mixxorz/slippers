---
sidebar_position: 2
---

# Examples

### Hello World

A very simple component that doesn't use `children`. It can be used like a
normal template tag.

```slippers title='Greeting: "greeting.html"'
<h1>Hello, {{ name }}!</h1>
```

```slippers title="Usage"
{% Greeting name="World" %}
```

```html title="Output"
<h1>Hello, World!</h1>
```

### Children

You can use the `children` prop to access the rendered template fragment passed
into the component block.

```slippers title='Alert: "alert.html"'
<div class="alert alert--{{ severity }}">
  <p class="alert__message">{{ children }}</p>
</div>
```

```slippers title="Usage"
{% #Alert severity="error" %}This is an error message{% /Alert %}
```

The opening tag is the component name prefixed with a `#` and the closing tag is
the component name prefixed with a `/`. The code within the block is passed to
the component as `children`. Other props can be passed in as usual.

```html title="Output"
<div class="alert alert--error">
  <p class="alert__message">This is an error message</p>
</div>
```

### Front matter

Components can include Python front matter. Code in the front matter is executed
immediately before the component is rendered.

```slippers title='Answer: "answer.html"'
---
props['answer'] = props['number'] * 42
---

<h1>{{ number }} times 42 is {{ answer }}</h1>
```

`props` is a special object that you can use to access the props passed to your
component. It can also be used to modify the props available in the template.

```slippers title="Usage"
{% Answer number=7 %}
```

```html title="Output"
<h1>7 times 42 is 294</h1>
```

### Default values

Default values for props can be specified using the `props.defaults` dictionary.

```slippers title='Button: "button.html"'
---
props.defaults = {
    'variant': 'primary',
}
---

<button class="button button-{{ variant }}">{{ children }}</button>
```

```slippers title="Usage"
{% #Button %}Primary button{% /Button %}
{% #Button variant="secondary" %}Secondary button{% /Button %}
```

```html title="Output"
<button class="button button-primary">Primary button</button>
<button class="button button-secondary">Secondary button</button>
```

### Prop types

Expected props and their types can be declared in the `props.types` dictionary.
Python's `typing` module is in scope which allows you to declare more complex
types.

Aside from documentation purposes, these prop types can be checked at runtime.
By default this is only enabled when `DEBUG` is `True`. The error messages
appear in the terminal and browser console.

```slippers title='Icon: "icon.html"'
---
props.types = {
    'name': Literal['checkmark', 'cross'],
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

```slippers title="Usage"
{% Icon name="checkmark" %}
{% Icon name="cross" variant="dark" size=24 %}
```

```html title="Output"
<span class="icon icon--light">
  <svg width="16" height="16">...checkmark svg...</svg>
</span>
<span class="icon icon--dark">
  <svg width="24" height="24">...cross svg...</svg>
</span>
```
