import re

from pygments.lexer import DelegatingLexer, RegexLexer, bygroups, include, using
from pygments.lexers.html import HtmlLexer
from pygments.lexers.python import PythonLexer
from pygments.token import Comment, Keyword, Name, Number, Operator, Other, Punctuation, String, Text


class SlippersTemplateLexer(RegexLexer):
    """
    Lexer for Slippers template tags
    Used as the overlay in SlippersLexer's DelegatingLexer composition.
    """

    name = "Slippers Template"
    aliases = []
    mimetypes = []

    flags = re.M | re.S

    tokens = {
        "root": [
            (r"[^{]+", Other),
            (r"\{\{", Comment.Preproc, "var"),
            # jinja/django comments
            (r"\{#.*?#\}", Comment),
            # django comments
            (
                r"(\{%)(-?\s*)(comment)(\s*-?)(%\})(.*?)" r"(\{%)(-?\s*)(endcomment)(\s*-?)(%\})",
                bygroups(
                    Comment.Preproc,
                    Text,
                    Keyword,
                    Text,
                    Comment.Preproc,
                    Comment,
                    Comment.Preproc,
                    Text,
                    Keyword,
                    Text,
                    Comment.Preproc,
                ),
            ),
            # raw jinja blocks
            (
                r"(\{%)(-?\s*)(raw)(\s*-?)(%\})(.*?)" r"(\{%)(-?\s*)(endraw)(\s*-?)(%\})",
                bygroups(
                    Comment.Preproc,
                    Text,
                    Keyword,
                    Text,
                    Comment.Preproc,
                    Text,
                    Comment.Preproc,
                    Text,
                    Keyword,
                    Text,
                    Comment.Preproc,
                ),
            ),
            # filter blocks
            (
                r"(\{%)(-?\s*)(filter)(\s+)([a-zA-Z_]\w*)",
                bygroups(Comment.Preproc, Text, Keyword, Text, Name.Function),
                "block",
            ),
            # Slippers opening component tag: {% #ComponentName %}
            (
                r"(\{%)(-?\s*)(#)([a-zA-Z_]\w*)",
                bygroups(Comment.Preproc, Text, Name.Tag, Name.Tag),
                "block",
            ),
            # Slippers closing component tag: {% /ComponentName %}
            (
                r"(\{%)(-?\s*)(/)([a-zA-Z_]\w*)",
                bygroups(Comment.Preproc, Text, Name.Tag, Name.Tag),
                "block",
            ),
            # Slippers inline component tag: {% ComponentName %} (PascalCase)
            (
                r"(\{%)(-?\s*)([A-Z][a-zA-Z_]\w*)",
                bygroups(Comment.Preproc, Text, Name.Tag),
                "block",
            ),
            # generic django/jinja tag
            (
                r"(\{%)(-?\s*)([a-zA-Z_]\w*)",
                bygroups(Comment.Preproc, Text, Keyword),
                "block",
            ),
            (r"\{", Other),
        ],
        "varnames": [
            (r"(\|)(\s*)([a-zA-Z_]\w*)", bygroups(Operator, Text, Name.Function)),
            (
                r"(is)(\s+)(not)?(\s+)?([a-zA-Z_]\w*)",
                bygroups(Keyword, Text, Keyword, Text, Name.Function),
            ),
            (r"(_|true|false|none|True|False|None)\b", Keyword.Pseudo),
            (
                r"(in|as|reversed|recursive|not|and|or|is|if|else|import|"
                r"with(?:(?:out)?\s*context)?|scoped|ignore\s+missing)\b",
                Keyword,
            ),
            (r"(loop|block|super|forloop)\b", Name.Builtin),
            (r"[a-zA-Z_][\w-]*", Name.Variable),
            (r"\.\w+", Name.Variable),
            (r':?"(\\\\|\\[^\\]|[^"\\])*"', String.Double),
            (r":?'(\\\\|\\[^\\]|[^'\\])*'", String.Single),
            (r"([{}()\[\]+\-*/%,:~]|[><=]=?|!=)", Operator),
            (r"[0-9](\.[0-9]*)?(eE[+-][0-9])?[flFLdD]?|0[xX][0-9a-fA-F]+[Ll]?", Number),
        ],
        "var": [
            (r"\s+", Text),
            (r"(-?)(\}\})", bygroups(Text, Comment.Preproc), "#pop"),
            include("varnames"),
        ],
        "block": [
            (r"\s+", Text),
            (r"(-?)(%\})", bygroups(Text, Comment.Preproc), "#pop"),
            include("varnames"),
            (r".", Punctuation),
        ],
    }


class SlippersHtmlLexer(DelegatingLexer):
    """Internal lexer: HTML + Slippers template tags, used by SlippersLexer."""

    name = "Slippers HTML"
    aliases = []
    mimetypes = []

    def __init__(self, **options):
        super().__init__(HtmlLexer, SlippersTemplateLexer, **options)


class SlippersLexer(RegexLexer):
    """
    Lexer for Slippers component files.

    Highlights an optional ``---`` delimited Python front matter block at the top,
    followed by the rest of the file as a Slippers/Django HTML template.
    """

    name = "Slippers"
    aliases = ["slippers"]
    mimetypes = ["application/x-slippers-templating"]

    flags = re.M | re.S

    tokens = {
        "root": [
            # Optional Python front matter: --- ... ---
            (
                r"(^---\n)(.*?)(^---\n)",
                bygroups(Comment.Preproc, using(PythonLexer), Comment.Preproc),
            ),
            # Rest of file is a Slippers/Django HTML template
            (r".+", using(SlippersHtmlLexer)),
        ],
    }
