#!/usr/bin/env python

# Wirth diagram draw.
# You will need cygwin (if you run this on Windows)
# cairo, pango, pycairo packages for Linux/Cygwin
# then you will need of course parcon Python library

from collections import OrderedDict

from parcon.railroad import Then, Or, Token, Loop, Bullet, Nothing
from parcon.railroad import PRODUCTION, TEXT
from parcon.railroad.raildraw import draw_to_png

production = lambda t: Token(PRODUCTION, t)
text = lambda t: Token(TEXT, t)

productions = OrderedDict([
    (
        "simple_filter",
        Then(
            Bullet(),
            Or(text("!"), Nothing()),
            text("null"), 
            Bullet()
        )
    ),
    (
        "filter",
        Then(
            Bullet(),
            Loop(
                Then(Or(text("!"), Nothing()), Or(production("term"),
                                                  Then(text("("), production("filter"), text(")")))),
                Or(
                   text("&"), text("|")
                   )
            ),
            Bullet()
        )
    ),
    (
        "numeric_term",
        Then(
            Bullet(),
            Or(
               text("null"),
               Then(production("<numeric literal>"), Or(
                   Then(text(".."), Or(production("<numeric literal>"), Nothing())), Nothing())),
               Then(Or(text(".."), text(">"), text("<")), production("<numeric literal>"))
            ),
            Bullet()
        )
    ),
    (
        "text_term",
        Then(
            Bullet(),
            Or(text("@"), Nothing()),
            Or(
               text("null"),
               Then(production("<text literal>"), Or(
                   Then(text(".."), Or(production("<text literal>"), Nothing())), Nothing())),
               Then(Or(text(".."), text(">"), text("<")), production("<text literal>")),
               Then(Or(text("%"), Nothing()), Loop( production("<text literal>"), text("%")), Or(text("%"), Nothing())),
            ),
            Bullet()
        )
    ),
    
])

options = {
    "raildraw_title_before":20,
    "raildraw_title_after": 30,
    "raildraw_scale": 2
}

i = 0
for pname in productions.keys():
    i += 1
    draw_to_png(OrderedDict([(pname, productions[pname])]), options,
                'target/filter/' + ('0' if i < 10 else '') + str(i) + '.' + pname +'.png', True)
