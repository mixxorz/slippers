---
sidebar_position: 1
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# Introduction

Slippers is a UI component framework for Django. It extends Django’s template language to provide better ergonomics around writing and using reusable UI components.

## Examples

### Hello World

```twig title='Greeting: "greeting.html"'
<h1>Hello, World!</h1>
```

```twig title="Template"
{% Greeting %}
```

```html title="Output"
<h1>Hello, World!</h1>
```

### Nested components

```twig title='Alert: "alert.html"'
<div class="alert">
  <span class="alert__icon"> {% AlertIcon severity=severity %} </span>

  <p class="alert__message">{{ children }}</p>
</div>
```

```twig title="Template"
{% #Alert severity="error" %}This is an error message{% /Alert %}
```

```twig title="Output"
<div class="alert">
  <span class="alert__icon">
    <svg>...</svg>
  </span>

  <p class="alert__message">This is an error message</p>
</div>
```

### Default values

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

### Custom logic

```twig title='Answer: "answer.html"'
---
props['answer'] = props['number'] * 42
---

<h1>{{ number }} times 42 is {{ answer }}</h1>
```

```twig title="Template"
{% Answer number=7 %}
```

```twig title="Output"
<h1>7 times 42 is 294</h1>
```

### Prop types

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
