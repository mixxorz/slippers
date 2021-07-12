from textwrap import dedent

from django.template import Context, Template
from django.test import TestCase


class InlineComponentTest(TestCase):
    def test_render(self):
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


class BlockComponentTest(TestCase):
    def test_render(self):
        template = Template(
            dedent(
                """
            {% load slippers %}

            {% button %}I am button{% endbutton %}
            """
            )
        )

        expected = dedent(
            """
            <button>I am button</button>
            """
        )

        self.assertHTMLEqual(expected, template.render(Context()))

    def test_render_nested(self):
        template = Template(
            dedent(
                """
            {% load slippers %}

            {% card heading="I am heading" %}
                {% button %}I am button{% endbutton %}
            {% endcard %}
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

    def test_render_filter_kwargs(self):
        template = Template(
            dedent(
                """
            {% load slippers %}

            {% card heading="I am heading"|upper %}
                {% button %}I am button{% endbutton %}
            {% endcard %}
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
