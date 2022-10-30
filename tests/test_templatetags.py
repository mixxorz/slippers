from django.template import Context, Template, TemplateSyntaxError
from django.test import TestCase, override_settings


class ComponentTest(TestCase):
    def test_render_inline_component(self):
        template = """
            {% avatar user="mixxorz" %}
        """

        expected = """
            <div>I am avatar for mixxorz</div>
        """

        self.assertHTMLEqual(expected, Template(template).render(Context()))

    def test_render_block_component(self):
        template = """
            {% #button %}I am button{% /button %}
        """

        expected = """
            <button>I am button</button>
        """

        self.assertHTMLEqual(expected, Template(template).render(Context()))

    def test_render_without_children(self):
        template = """
            {% icon_button icon="envelope" %}
            {% #icon_button icon="envelope" %}Submit{% /icon_button %}
        """

        expected = """
            <button class="icon-button envelope"></button>
            <button class="icon-button envelope">Submit</button>
        """

        self.assertHTMLEqual(expected, Template(template).render(Context()))

    def test_render_nested(self):
        template = """
            {% #card heading="I am heading" %}
            {% #button %}I am button{% /button %}
            {% /card %}
        """

        expected = """
            <div class="card">
                <div class="card__header">I am heading</div>
                <div class="card__body">
                    <button>I am button</button>
                </div>
            </div>
        """

        self.assertHTMLEqual(expected, Template(template).render(Context()))

    def test_kwargs_with_filters(self):
        template = """
            {% #card heading="I am heading"|upper %}
            {% #button %}I am button{% /button %}
            {% /card %}
        """

        expected = """
            <div class="card">
                <div class="card__header">I AM HEADING</div>
                <div class="card__body">
                    <button>I am button</button>
                </div>
            </div>
        """

        self.assertHTMLEqual(expected, Template(template).render(Context()))

    def test_render_as_variable(self):
        template = """
            {% avatar user="mixxorz" as my_avatar %}
            {% #button as my_button %}I am button{% /button %}


            <div>
                {{ my_avatar }}
                {{ my_button }}
            </div>
        """

        expected = """
            <div>
                <div>I am avatar for mixxorz</div>
                <button>I am button</button>
            </div>
        """

        self.assertHTMLEqual(expected, Template(template).render(Context()))

    def test_pass_boolean_flags(self):
        template = """
            {% #button disabled %}I am button{% /button %}
        """

        expected = """
            <button disabled>I am button</button>
            """

        self.assertHTMLEqual(expected, Template(template).render(Context()))

    def test_pass_boolean_flags_with_other_arguments(self):
        template = """
            {% #button disabled class="foo" %}I am button{% /button %}
        """

        expected = """
            <button disabled class="foo">I am button</button>
            """

        self.assertHTMLEqual(expected, Template(template).render(Context()))

    def test_pass_special_symbols(self):
        template = """
            {% special_attributes x-data="controller" x-bind:class="bind-class" @click="myHandler" %}
        """

        expected = """
            <div x-data="controller" x-bind:class="bind-class" @click="myHandler"></div>
            """

        self.assertHTMLEqual(expected, Template(template).render(Context()))


class FrontMatterTest(TestCase):
    def test_strips_out_front_matter(self):
        template = """
            {% type_checking string="Hello" number=10 list_of_numbers=numbers string_or_number="ten" %}
        """

        expected = """
            <div>
                String: Hello
                Number: 10
                List of numbers: [1, 2, 3]
                Optional string:
                String or number: ten
            </div>
        """

        self.assertHTMLEqual(
            expected, Template(template).render(Context({"numbers": [1, 2, 3]}))
        )

    def test_warning_for_invalid_prop_types(self):
        template = """
            {% type_checking string=10 number="ten" list_of_numbers=numbers %}
        """

        # Message format is:
        # Invalid prop 'key' passed to 'tag_name'. Expected 'int', got 'str' instead.
        expected_warnings = [
            "WARNING:slippers:Invalid prop `string` passed to `type_checking`. Expected `str`, got `int` instead.",
            "WARNING:slippers:Invalid prop `number` passed to `type_checking`. Expected `int`, got "
            "`django.utils.safestring.SafeString` instead.",
            "WARNING:slippers:Invalid prop `list_of_numbers` passed to `type_checking`. Expected `List[int]`, got "
            "`list` instead.",
        ]

        with self.assertLogs("slippers", level="WARNING") as cm:
            Template(template).render(Context({"numbers": [1, "two"]}))

            for warning in expected_warnings:
                self.assertIn(warning, cm.output)

    def test_warning_for_required_props(self):
        template = """
            {% type_checking string="Hello" number=10 %}
        """

        # Message format is:
        # Required prop 'key' was not passed to 'tag_name'.
        expected_warnings = [
            "WARNING:slippers:Required prop `list_of_numbers` was not passed to `type_checking`.",
            "WARNING:slippers:Required prop `string_or_number` was not passed to `type_checking`.",
        ]

        with self.assertLogs("slippers", level="WARNING") as cm:
            Template(template).render(Context())

            for warning in expected_warnings:
                self.assertIn(warning, cm.output)

    def test_warning_for_extra_props(self):
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

        template = """
            <input {% attrs type id name %}>
        """

        expected = """
            <input type="text" id="the_id" name="the_name">
        """

        self.assertHTMLEqual(expected, Template(template).render(context))

    def test_with_hyphens(self):
        context = Context(
            {
                "aria-label": "Search",
            }
        )

        template = """
            <input {% attrs aria-label %}>
        """

        expected = """
            <input aria-label="Search">
        """

        self.assertHTMLEqual(expected, Template(template).render(context))

    def test_with_hyphens_legacy(self):
        context = Context(
            {
                "aria_label": "Search",
            }
        )

        template = """
            <input {% attrs aria_label %}>
        """

        expected = """
            <input aria-label="Search">
        """

        with self.assertWarns(DeprecationWarning):
            output = Template(template).render(context)

        self.assertHTMLEqual(expected, output)

    def test_with_colons(self):
        context = Context(
            {
                "x-bind:class": "my-class",
            }
        )

        template = """
            <input {% attrs x-bind:class %}>
        """

        expected = """
            <input x-bind:class="my-class">
        """

        self.assertHTMLEqual(expected, Template(template).render(context))

    def test_with_at_symbol(self):
        context = Context(
            {
                "@click": "myHandler",
            }
        )

        template = """
            <button {% attrs @click %}>Click me</button>
        """

        expected = """
            <button @click="myHandler">Click me</button>
        """

        self.assertHTMLEqual(expected, Template(template).render(context))

    def test_boolean_values(self):
        context = Context(
            {
                "autofocus": False,
                "disabled": True,
            }
        )

        template = """
            <button {% attrs autofocus disabled %}>Click me</button>
        """

        expected = """
            <button disabled>Click me</button>
        """

        self.assertHTMLEqual(expected, Template(template).render(context))

    def test_source_name(self):
        context = Context(
            {
                "input_type": "text",
                "id": "the_id",
                "name": "the_name",
            }
        )

        template = """
            <input {% attrs type=input_type id name %}>
        """

        expected = """
            <input type="text" id="the_id" name="the_name">
        """

        self.assertHTMLEqual(expected, Template(template).render(context))


class VarTagTest(TestCase):
    def test_basic(self):
        template = """
            {% var foo="Hello, World!" %}

            <div>{{ foo }}</div>
        """

        expected = """
            <div>Hello, World!</div>
        """

        self.assertHTMLEqual(expected, Template(template).render(Context()))

    def test_value_filter(self):
        template = """
            {% var foo=foo|default:"Default value" %}
            {% var bar="Hello, World!"|upper %}

            <div>{{ foo }}</div>
            <div>{{ bar }}</div>
        """

        expected = """
            <div>Default value</div>
            <div>HELLO, WORLD!</div>
        """

        self.assertHTMLEqual(expected, Template(template).render(Context()))

    def test_special_characters(self):
        template = """
            {% var title="My title" %}
            {% var x-bind:class="foo" %}
            {% var @click="myHandler" %}

            <div {% attrs x-bind:class @click %}>{{ title }}</div>
        """

        expected = """
        <div x-bind:class="foo" @click="myHandler">My title</div>
        """

        self.assertHTMLEqual(expected, Template(template).render(Context()))


class MatchFilterTest(TestCase):
    def test_basic(self):
        context = Context({"first": "outline", "second": "ghost", "third": "square"})

        template = """
            <button class="{{ first|match:"outline:btn-outline,ghost:btn-ghost" }}">Click me</button>
            <button class="{{ second|match:"outline:btn-outline,ghost:btn-ghost" }}">Click me</button>
            <button class="{{ third|match:"outline:btn-outline,ghost:btn-ghost" }}">Click me</button>
        """

        expected = """
            <button class="btn-outline">Click me</button>
            <button class="btn-ghost">Click me</button>
            <button class="">Click me</button>
        """

        self.assertHTMLEqual(expected, Template(template).render(context))

    @override_settings(DEBUG=True)
    def test_syntax_error(self):
        template = """
            <button class="{{ "foo"|match:"outline:btn-outline,foo:bar:baz,,:apple,:orange" }}">Click me</button>
        """

        with self.assertRaises(TemplateSyntaxError):
            Template(template).render(Context())

    def test_ignore_spaces(self):
        context = Context({"variant": "ghost"})

        template = """
            <button class="{{ variant|match:"outline:btn-outline, ghost:btn-ghost" }}">Click me</button>
        """

        expected = """
            <button class="btn-ghost">Click me</button>
        """

        self.assertHTMLEqual(expected, Template(template).render(context))


class FragmentTagTest(TestCase):
    def test_basic(self):
        context = Context({})

        template = """
            {% fragment as my_fragment %}
            <p>Hello, World</p>
            {% endfragment %}

            Text coming after:
            {{ my_fragment }}
        """

        expected = """
            Text coming after:
            <p>Hello, World</p>
        """

        self.assertHTMLEqual(expected, Template(template).render(context))

    @override_settings(DEBUG=True)
    def test_syntax_error(self):
        template = """
            {% fragment %}
            <p>Hello, World</p>
            {% endfragment %}
        """

        with self.assertRaises(TemplateSyntaxError):
            Template(template).render(Context())

    def test_with_variables(self):
        context = Context({"name": "jonathan wells"})

        template = """
            {% fragment as my_fragment %}
                <p>Hello, {{ name|title }}</p>
            {% endfragment %}

            Text coming after:
            {{ my_fragment }}
        """

        expected = """
            Text coming after:
            <p>Hello, Jonathan Wells</p>
        """

        self.assertHTMLEqual(expected, Template(template).render(context))
