from pygments.lexers import _lexer_cache
from pygments.lexers._mapping import LEXERS

from pygments_slippers import SlippersLexer


def on_config(config):
    LEXERS[SlippersLexer.__name__] = (
        SlippersLexer.__module__,
        SlippersLexer.name,
        tuple(SlippersLexer.aliases),
        (),
        tuple(SlippersLexer.mimetypes),
    )
    _lexer_cache[SlippersLexer.name] = SlippersLexer
