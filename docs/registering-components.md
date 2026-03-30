# Registering components

Components can be registered through the `components.yaml` file. This file should be placed at the root template directory.

```yaml title="myapp/templates/components.yaml"
components:
  Card: "myapp/card.html"
  Button: "myapp/button.html"
  Icon: "myapp/icon.html"
  IconButton: "myapp/icon_button.html"
```

The key is used as the name of the component, and the value is the path to the component template.

## Other ways to register components

If you have special requirements, or simply prefer an alternative way of registering components, you can use the `register_components` function directly.

```python
from slippers.templatetags.slippers import register_components

register_components({
  "Card": "myapp/card.html",
  "Button": "myapp/button.html",
})
```

## Adding components to a different register

By default, the above methods will register components to the `slippers` tag register. This means that you need to load the `slippers` template tags before being able to use the components (`{% load slippers %}`).

There may be cases where you want to register the components to a different tag register; for instance, if you're building a reusable component library.

To do this, you need to pass your own `register` to the `register_components` function.

```python title="my_library/templatetags/my_components.py"
from django import template

register = template.Library()

register_components({
  "Card": "my_library/card.html",
  "Button": "my_library/button.html",
}, register)
```

Now you can use the components by loading the `my_components` template tags.

```slippers
{% load my_components %}

{% #Button %}My button{% /Button %}
```
