"""
Overrides for the Django Template system to allow finer control over template parsing.
"""

import re

from django.template.base import (
    FILTER_ARGUMENT_SEPARATOR,
    FILTER_SEPARATOR,
    FilterExpression,
    TemplateSyntaxError,
    Variable,
    VariableDoesNotExist,
    constant_string,
)
from django.utils.regex_helper import _lazy_re_compile

########################################################################################################################
# Custom FilterExpression
#
# This is a copy of the original FilterExpression. The only difference is to allow variable names to have extra special
# characters: -, :, and @
########################################################################################################################
filter_raw_string = r"""
^(?P<constant>{constant})|
^(?P<var>[{var_chars}]+|{num})|
 (?:\s*{filter_sep}\s*
     (?P<filter_name>\w+)
         (?:{arg_sep}
             (?:
              (?P<constant_arg>{constant})|
              (?P<var_arg>[{var_chars}]+|{num})
             )
         )?
 )""".format(
    constant=constant_string,
    num=r"[-+\.]?\d[\d\.e]*",
    # The following is the only difference from the original FilterExpression. We allow variable names to have extra
    # special characters: -, :, and @
    var_chars=r"\w\-\:\@\.",
    filter_sep=re.escape(FILTER_SEPARATOR),
    arg_sep=re.escape(FILTER_ARGUMENT_SEPARATOR),
)

filter_re = _lazy_re_compile(filter_raw_string, re.VERBOSE)


class SlippersFilterExpression(FilterExpression):
    def __init__(self, token, parser):
        # This method is exactly the same as the original FilterExpression.__init__ method, the only difference being
        # the value of `filter_re`.
        self.token = token
        matches = filter_re.finditer(token)
        var_obj = None
        filters = []
        upto = 0
        for match in matches:
            start = match.start()
            if upto != start:
                raise TemplateSyntaxError(
                    "Could not parse some characters: "
                    "%s|%s|%s" % (token[:upto], token[upto:start], token[start:])
                )
            if var_obj is None:
                var, constant = match["var"], match["constant"]
                if constant:
                    try:
                        var_obj = Variable(constant).resolve({})
                    except VariableDoesNotExist:
                        var_obj = None
                elif var is None:
                    raise TemplateSyntaxError(
                        "Could not find variable at " "start of %s." % token
                    )
                else:
                    var_obj = Variable(var)
            else:
                filter_name = match["filter_name"]
                args = []
                constant_arg, var_arg = match["constant_arg"], match["var_arg"]
                if constant_arg:
                    args.append((False, Variable(constant_arg).resolve({})))
                elif var_arg:
                    args.append((True, Variable(var_arg)))
                filter_func = parser.find_filter(filter_name)
                self.args_check(filter_name, filter_func, args)  # type: ignore
                filters.append((filter_func, args))
            upto = match.end()
        if upto != len(token):
            raise TemplateSyntaxError(
                "Could not parse the remainder: '%s' "
                "from '%s'" % (token[upto:], token)
            )

        self.filters = filters
        self.var = var_obj
        self.is_var = isinstance(var_obj, Variable)


########################################################################################################################
# Custom token_kwargs
#
# Same as the original token_kwargs, but uses the SlippersFilterExpression instead of the original FilterExpression.
########################################################################################################################

# Regex for token keyword arguments
kwarg_re = _lazy_re_compile(r"(?:([\w\-\:\@]+)=)?(.+)")


def slippers_token_kwargs(bits, parser, support_legacy=False):
    """
    Parse token keyword arguments and return a dictionary of the arguments
    retrieved from the ``bits`` token list.

    `bits` is a list containing the remainder of the token (split by spaces)
    that is to be checked for arguments. Valid arguments are removed from this
    list.

    `support_legacy` - if True, the legacy format ``1 as foo`` is accepted.
    Otherwise, only the standard ``foo=1`` format is allowed.

    There is no requirement for all remaining token ``bits`` to be keyword
    arguments, so return the dictionary as soon as an invalid argument format
    is reached.
    """
    if not bits:
        return {}
    match = kwarg_re.match(bits[0])
    kwarg_format = match and match[1]
    if not kwarg_format:
        if not support_legacy:
            return {}
        if len(bits) < 3 or bits[1] != "as":
            return {}

    kwargs = {}
    while bits:
        if kwarg_format:
            match = kwarg_re.match(bits[0])
            if not match or not match[1]:
                return kwargs
            key, value = match.groups()
            del bits[:1]
        else:
            if len(bits) < 3 or bits[1] != "as":
                return kwargs
            key, value = bits[2], bits[0]
            del bits[:3]

        # This is the only difference from the original token_kwargs. We use the SlippersFilterExpression instead of the
        # original FilterExpression.
        kwargs[key] = SlippersFilterExpression(value, parser)
        if bits and not kwarg_format:
            if bits[0] != "and":
                return kwargs
            del bits[:1]
    return kwargs
