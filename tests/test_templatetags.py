from textwrap import dedent

from django.template import Context, Template, TemplateSyntaxError
from django.test import TestCase, override_settings


class ComponentTest(TestCase):
    def test_render_inline_component(self):
        template = Template(
            dedent(
                """
            {% load slippers %}

            {% avatar user="mixxorz" %}
            """
            )
        )

        expected = dedent(
            """
            <div>I am avatar for mixxorz</div>
            """
        )

        self.assertHTMLEqual(expected, template.render(Context()))

    def test_render_block_component(self):
        template = Template(
            dedent(
                """
            {% load slippers %}

            {% #button %}I am button{% /button %}
            """
            )
        )

        expected = dedent(
            """
            <button>I am button</button>
            """
        )

        self.assertHTMLEqual(expected, template.render(Context()))

    def test_render_without_children(self):
        template = Template(
            dedent(
                """
            {% load slippers %}

            {% icon_button icon="envelope" %}
            {% #icon_button icon="envelope" %}Submit{% /icon_button %}
            """
            )
        )

        expected = dedent(
            """
            <button class="icon-button envelope"></button>
            <button class="icon-button envelope">Submit</button>
            """
        )

        self.assertHTMLEqual(expected, template.render(Context()))

    def test_render_nested(self):
        template = Template(
            dedent(
                """
            {% load slippers %}

            {% #card heading="I am heading" %}
                {% #button %}I am button{% /button %}
            {% /card %}
            """
            )
        )

        expected = dedent(
            """
            <div class="card">
                <div class="card__header">I am heading</div>
                <div class="card__body">
                    <button>I am button</button>
                </div>
            </div>
            """
        )

        self.assertHTMLEqual(expected, template.render(Context()))

    def test_kwargs_with_filters(self):
        template = Template(
            dedent(
                """
            {% load slippers %}

            {% #card heading="I am heading"|upper %}
                {% #button %}I am button{% /button %}
            {% /card %}
            """
            )
        )

        expected = dedent(
            """
            <div class="card">
                <div class="card__header">I AM HEADING</div>
                <div class="card__body">
                    <button>I am button</button>
                </div>
            </div>
            """
        )

        self.assertHTMLEqual(expected, template.render(Context()))

    def test_render_as_variable(self):
        template = Template(
            dedent(
                """
            {% load slippers %}

            {% avatar user="mixxorz" as my_avatar %}
            {% #button as my_button %}I am button{% /button %}


            <div>
                {{ my_avatar }}
                {{ my_button }}
            </div>
            """
            )
        )

        expected = dedent(
            """
            <div>
                <div>I am avatar for mixxorz</div>
                <button>I am button</button>
            </div>
            """
        )

        self.assertHTMLEqual(expected, template.render(Context()))

    def test_pass_boolean_flags(self):
        self.fail()


class AttrsTagTest(TestCase):
    def test_basic(self):
        context = Context(
            {
                "type": "text",
                "id": "the_id",
                "name": "the_name",
            }
        )

        template = dedent(
            """
            {% load slippers %}

            <input {% attrs type id name %}>
            """
        )

        expected = dedent(
            """
            <input type="text" id="the_id" name="the_name">
            """
        )

        self.assertHTMLEqual(expected, Template(template).render(context))

    def test_boolean_values(self):
        context = Context(
            {
                "autofocus": False,
                "disabled": True,
            }
        )

        template = dedent(
            """
            {% load slippers %}

            <button {% attrs autofocus disabled %}>Click me</button>
            """
        )

        expected = dedent(
            """
            <button disabled>Click me</button>
            """
        )

        self.assertHTMLEqual(expected, Template(template).render(context))

    def test_source_name(self):
        context = Context(
            {
                "input_type": "text",
                "id": "the_id",
                "name": "the_name",
            }
        )

        template = dedent(
            """
            {% load slippers %}

            <input {% attrs type=input_type id name %}>
            """
        )

        expected = dedent(
            """
            <input type="text" id="the_id" name="the_name">
            """
        )

        self.assertHTMLEqual(expected, Template(template).render(context))


class VarTagTest(TestCase):
    def test_basic(self):
        context = Context()

        template = dedent(
            """
            {% load slippers %}

            {% var foo="Hello, World!" %}

            <div>{{ foo }}</div>
            """
        )

        expected = dedent(
            """
            <div>Hello, World!</div>
            """
        )

        self.assertHTMLEqual(expected, Template(template).render(context))

    def test_value_filter(self):
        context = Context()

        template = dedent(
            """
            {% load slippers %}

            {% var foo=foo|default:"Default value" %}
            {% var bar="Hello, World!"|upper %}

            <div>{{ foo }}</div>
            <div>{{ bar }}</div>
            """
        )

        expected = dedent(
            """
            <div>Default value</div>
            <div>HELLO, WORLD!</div>
            """
        )

        self.assertHTMLEqual(expected, Template(template).render(context))


class MatchFilterTest(TestCase):
    def test_basic(self):
        context = Context({"first": "outline", "second": "ghost", "third": "square"})

        template = dedent(
            """
            {% load slippers %}

            <button class="{{ first|match:"outline:btn-outline,ghost:btn-ghost" }}">Click me</button>
            <button class="{{ second|match:"outline:btn-outline,ghost:btn-ghost" }}">Click me</button>
            <button class="{{ third|match:"outline:btn-outline,ghost:btn-ghost" }}">Click me</button>
            """
        )

        expected = dedent(
            """
            <button class="btn-outline">Click me</button>
            <button class="btn-ghost">Click me</button>
            <button class="">Click me</button>
            """
        )

        self.assertHTMLEqual(expected, Template(template).render(context))

    @override_settings(DEBUG=True)
    def test_syntax_error(self):
        context = Context()

        template = dedent(
            """
            {% load slippers %}

            <button class="{{ "foo"|match:"outline:btn-outline,foo:bar:baz,,:apple,:orange" }}">Click me</button>
            """
        )

        with self.assertRaises(TemplateSyntaxError):
            Template(template).render(context)

    def test_ignore_spaces(self):
        context = Context({"variant": "ghost"})

        template = dedent(
            """
            {% load slippers %}

            <button class="{{ variant|match:"outline:btn-outline, ghost:btn-ghost" }}">Click me</button>
            """
        )

        expected = dedent(
            """
            <button class="btn-ghost">Click me</button>
            """
        )

        self.assertHTMLEqual(expected, Template(template).render(context))
