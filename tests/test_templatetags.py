from unittest.mock import patch

from django.conf import settings as django_settings
from django.template import Context, Template, TemplateSyntaxError
from django.test import TestCase, override_settings

from typeguard import get_type_name


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


@override_settings(SLIPPERS_RUNTIME_TYPE_CHECKING=True)
class PropsTest(TestCase):
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

        output = Template(template).render(Context({"numbers": [1, 2, 3]}))

        self.assertInHTML(expected, output)

    @patch("slippers.templatetags.slippers.render_error_html")
    def test_warning_for_invalid_prop_types(self, mock_render_error_html):
        mock_render_error_html.return_value = ""

        template = """
            {% type_checking string=10 number="ten" list_of_numbers=numbers string_or_number=10 %}
        """
        expected_errors = [
            # (prop_name, expected_type, actual_type)
            ("string", "str", "int"),
            ("number", "int", "django.utils.safestring.SafeString"),
            ("list_of_numbers", "List[int]", "list"),
        ]

        Template(template).render(Context({"numbers": [1, "two"]}))

        # Check browser errors
        browser_errors = mock_render_error_html.call_args[1]["errors"]

        self.assertEqual(len(expected_errors), len(browser_errors))

        for expected_error, actual_error in zip(expected_errors, browser_errors):
            with self.subTest(prop=expected_error[0]):
                self.assertEqual("invalid", actual_error.error)
                self.assertEqual(expected_error[0], actual_error.name)
                self.assertEqual(
                    expected_error[1], get_type_name(actual_error.expected)
                )
                self.assertEqual(expected_error[2], get_type_name(actual_error.actual))

    @patch("slippers.templatetags.slippers.render_error_html")
    def test_warning_for_required_props(self, mock_render_error_html):
        mock_render_error_html.return_value = ""

        template = """
            {% type_checking string="Hello" number=10 %}
        """
        expected_errors = [
            # (prop_name, expected_type, actual_type)
            ("list_of_numbers", "List[int]", "NoneType"),
            ("string_or_number", "Union[str, int]", "NoneType"),
        ]

        Template(template).render(Context())

        # Check browser errors
        browser_errors = mock_render_error_html.call_args[1]["errors"]

        self.assertEqual(len(expected_errors), len(browser_errors))

        for expected_error, actual_error in zip(expected_errors, browser_errors):
            with self.subTest(prop=expected_error[0]):
                self.assertEqual("missing", actual_error.error)
                self.assertEqual(expected_error[0], actual_error.name)
                self.assertEqual(
                    expected_error[1], get_type_name(actual_error.expected)
                )
                self.assertEqual(expected_error[2], get_type_name(actual_error.actual))

    @patch("slippers.templatetags.slippers.render_error_html")
    def test_warning_for_extra_props(self, mock_render_error_html):
        mock_render_error_html.return_value = ""

        template = """
            {% type_checking string="Hello" number=10 list_of_numbers=numbers string_or_number="ten" extra="foo" %}
        """
        expected_errors = [
            # (prop_name, expected_type, actual_type)
            ("extra", "NoneType", "django.utils.safestring.SafeString"),
        ]

        Template(template).render(Context({"numbers": [1, 2, 3]}))

        # Check browser errors
        browser_errors = mock_render_error_html.call_args[1]["errors"]

        self.assertEqual(len(expected_errors), len(browser_errors))

        for expected_error, actual_error in zip(expected_errors, browser_errors):
            with self.subTest(prop=expected_error[0]):
                self.assertEqual("extra", actual_error.error)
                self.assertEqual(expected_error[0], actual_error.name)
                self.assertEqual(
                    expected_error[1], get_type_name(actual_error.expected)
                )
                self.assertEqual(expected_error[2], get_type_name(actual_error.actual))

    @override_settings()
    @patch("slippers.templatetags.slippers.check_prop_types")
    def test_runtime_type_checking_settings(self, mock_check_prop_types):
        template = """
            {% type_checking string=10 number="ten" list_of_numbers=numbers string_or_number=10 %}
        """
        mock_check_prop_types.return_value = []

        # Delete the setting set by override_settings on the class
        del django_settings.SLIPPERS_RUNTIME_TYPE_CHECKING  # type: ignore

        # SLIPPERS_RUNTIME_TYPE_CHECKING is set
        with self.subTest(SLIPPERS_RUNTIME_TYPE_CHECKING=False), self.settings(
            SLIPPERS_RUNTIME_TYPE_CHECKING=False
        ):
            Template(template).render(Context({"numbers": [1, "two"]}))

            self.assertFalse(mock_check_prop_types.called)

        # SLIPPERS_RUNTIME_TYPE_CHECKING is not set, it should fallback to the value of DEBUG
        with self.subTest(DEBUG=False), self.settings(DEBUG=False):
            Template(template).render(Context({"numbers": [1, "two"]}))

            self.assertFalse(mock_check_prop_types.called)

        with self.subTest(DEBUG=True), self.settings(DEBUG=True):
            Template(template).render(Context({"numbers": [1, "two"]}))

            self.assertTrue(mock_check_prop_types.called)

    @patch("slippers.templatetags.slippers.render_error_html")
    def test_type_checking_output(self, mock_render_error_html):
        mock_render_error_html.return_value = ""

        template = """
            {% type_checking %}
        """
        with self.subTest("overlay"), self.settings(
            SLIPPERS_TYPE_CHECKING_OUTPUT=["overlay"]
        ):
            Template(template).render(Context())

            self.assertTrue(mock_render_error_html.called)

        mock_render_error_html.reset_mock()

        with self.subTest("console"), self.settings(
            SLIPPERS_TYPE_CHECKING_OUTPUT=["console"]
        ):
            Template(template).render(Context())

            self.assertTrue(mock_render_error_html.called)


class ErrorUITest(TestCase):
    def test_render_error_ui(self):
        template = """
            {% slippers_overlay %}
        """

        with self.subTest("Enabled"), self.settings(
            SLIPPERS_RUNTIME_TYPE_CHECKING=True
        ):
            output = Template(template).render(Context())
            self.assertIn("slippers_errors_ui_root", output)

        with self.subTest("Disabled"), self.settings(
            SLIPPERS_RUNTIME_TYPE_CHECKING=False
        ):
            output = Template(template).render(Context())
            self.assertNotIn("slippers_errors_ui_root", output)

    def test_type_checking_output(self):
        template = """
            {% slippers_overlay %}
        """
        with self.settings(SLIPPERS_RUNTIME_TYPE_CHECKING=True):
            output = Template(template).render(Context())
            self.assertIn('["console", "overlay"]', output)


@override_settings(SLIPPERS_RUNTIME_TYPE_CHECKING=True)
class ComponentCodeTest(TestCase):
    @patch("slippers.templatetags.slippers.render_error_html")
    def test_component_code(self, mock_render_error_html):
        mock_render_error_html.return_value = ""

        template = """
            {% component_code required_string="Hello, World" %}
        """

        expected = """
            The context contains:

            Required string: Hello, World
            Optional number:
            Default number: 10
            New number: 20
        """

        output = Template(template).render(Context())

        self.assertHTMLEqual(expected, output)

        # Check that declaring new_number in front_matter doesn't trigger type errors
        # new_number isn't in the type declaration, but it still shouldn't trigger an error as it was declared within
        # the front_matter and not passed in externally
        self.assertFalse(mock_render_error_html.called)


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
