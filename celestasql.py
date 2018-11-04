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
        "script",
        Then(
            Bullet(),
            production("create_grain"),
            Loop(text(";"),
                 Or(
                     production("create_sequence"),
                     production("create_table"),
                     production("add_foreign_key"),
                     production("create_index"),
                     production("create_view"),
                     production("create_materialized_view"),
                     production("create_function")
                 )
                 ),
            Bullet()
        )
    ),
    (
        "create_grain",
        Then(
            Bullet(),
            text("CREATE"),
            Or(text("GRAIN"),
               text("SCHEMA")),
            production("<grain name>"),
            text("VERSION"),
            text("'"),
            production("<grain version tag>"),
            text("'"),
            Or(
                Nothing(),
                Then(text("WITH"), text("NO"), text("AUTOUPDATE"))
            ),
            Bullet()
        )
    ),
    (
        "create_sequence",
        Then(
            Bullet(),
            text("CREATE"),
            text("SEQUENCE"),
            production("<sequence name>"),
            Loop(
                Or(
                    Then(text("START"), text("WITH"), production("<integer literal>")),
                    Then(text("INCREMENT"), text("BY"), production("<integer literal>")),
                    Then(text("MINVALUE"), production("<integer literal>")),
                    Then(text("MAXVALUE"), production("<integer literal>")),
                    text("CYCLE")
                ),
                Nothing()
            ),
            Bullet()
        )
    ),
    (
        "create_table",
        Then(
            Bullet(),
            text("CREATE"),
            text("TABLE"),
            production("<table name>"),
            text("("),
            Loop(
                production("table_constituent"),
                text(",")
            ),
            text(")"),
            Or(production("table_options"), Nothing()),
            Bullet()
        )
    ),
    ("table_constituent",
     Then(
         Bullet(),
         Or(
             production("field_definition"),
             Then(
                 Or(
                     Then(text("CONSTRAINT"), production("<pk name>")),
                     Nothing()
                 ),
                 production("primary_key_definition")
             ),
             Then(
                 Or(
                     Then(text("CONSTRAINT"), production("<fk name>")),
                     Nothing()
                 ),
                 production("foreign_key_definition")
             )
         ),
         Bullet()
     )
     ),
    (
        "table_options",
        Then(
            Bullet(),
            text("WITH"),
            Or(
                Then(text("READ"), text("ONLY")),
                Then(Or(text("NO"), Nothing()), text("VERSION"), text("CHECK"))
            ),
            Or(
                Nothing(),
                Then(text("NO"), text("AUTOUPDATE"))
            ),
            Bullet()
        )
    ),
    (
        "field_definition",
        Then(
            Bullet(),
            production("<field name>"),
            Or(
                production("int_field"),
                production("floating_field"),
                production("decimal_field"),
                production("text_field"),
                production("blob_field"),
                production("datetime_field"),
                production("datetime_with_time_zone_field"),
                production("bit_field")
            ),
            Or(
                Then(text("PRIMARY"), text("KEY")),
                Nothing()
            ),
            Or(
                Then(production("inline_fk_definition")),
                Nothing()
            ),
            Bullet()
        )
    ),
    (
        "inline_fk_definition",
        Then(
            Bullet(),
            text("FOREIGN"),
            text("KEY"),
            text("REFERENCES"),
            production("table_ref"),
            text("("),
            production("<field name>"),
            text(")"),
            production("fk_rules"),
            Bullet()
        )
    ),
    (
        "table_ref",
        Then(
            Bullet(),
            Or(Then(production("<grain name>"), text(".")), Nothing()),
            production("<table name>"),
            Bullet()
        )
    ),
    ("fk_rules",
     Then(
         Bullet(),
         Or(
             Then(text("ON"), text("UPDATE"),
                  Or(Then(text("NO"), text("ACTION")), text("CASCADE"), Then(text("SET"), text("NULL")))),
             Nothing()
         ),
         Or(
             Then(text("ON"), text("DELETE"),
                  Or(Then(text("NO"), text("ACTION")), text("CASCADE"), Then(text("SET"), text("NULL")))),
             Nothing()
         ),
         Bullet()
     )
     ),
    (
        "int_field",
        Then(
            Bullet(),
            text("INT"),
            Then(Or(Then(Or(text("NOT"), Nothing()), text("NULL")), Nothing())),
            Or(
                Then(
                    text("DEFAULT"),
                    Or(
                        production("<integer literal>"),
                        Then(text('NEXTVAL'), text('('), production("<sequence name>"), text(')'))
                    )
                ),
                Nothing()
            ),
            Bullet()
        )
    ),
    (
        "floating_field",
        Then(
            Bullet(),
            text("REAL"),
            Then(Or(Then(Or(text("NOT"), Nothing()), text("NULL")), Nothing())),
            Or(Then(text("DEFAULT"), production("<float.-point literal>")), Nothing()),
            Bullet()
        )
    ),
    (
        "decimal_field",
        Then(
            Bullet(),
            text("DECIMAL"),
            text("("), production("<integer literal>"), text(","), production("<integer literal>"), text(")"),
            Then(Or(Then(Or(text("NOT"), Nothing()), text("NULL")), Nothing())),
            Or(Then(text("DEFAULT"), production("<float.-point literal>")), Nothing()),
            Bullet()
        )
    ),
    (
        "text_field",
        Then(
            Bullet(),
            Or(Then(text("VARCHAR"), text("("), production("<integer literal>"), text(")")),
               text("TEXT")),
            Then(Or(Then(Or(text("NOT"), Nothing()), text("NULL")), Nothing())),
            Or(Then(text("DEFAULT"), production("<text literal>")), Nothing()),
            Bullet()
        )
    ),
    (
        "blob_field",
        Then(
            Bullet(),
            text("BLOB"),
            Then(Or(Then(Or(text("NOT"), Nothing()), text("NULL")), Nothing())),
            Or(Then(text("DEFAULT"), production("<binary literal>")), Nothing()),
            Bullet()
        )
    ),
    (
        "datetime_field",
        Then(
            Bullet(),
            text("DATETIME"),
            Then(Or(Then(Or(text("NOT"), Nothing()), text("NULL")), Nothing())),
            Or(Then(text("DEFAULT"),
                    Or(Then(text("'"), production("<YYYYMMDD>"), text("'")), text("GETDATE()"))), Nothing()),
            Bullet()
        )
    ),
    (
        "datetime_with_time_zone_field",
        Then(
            Bullet(),
            text("DATETIME"),
            text("WITH"),
            text("TIME"),
            text("ZONE"),
            Then(Or(Then(Or(text("NOT"), Nothing()), text("NULL")), Nothing())),
            Bullet()
        )
    ),
    (
        "bit_field",
        Then(
            Bullet(),
            text("BIT"),
            Then(Or(Then(Or(text("NOT"), Nothing()), text("NULL")), Nothing())),
            Or(Then(text("DEFAULT"), Or(text("'TRUE'"), text("'FALSE'"))), Nothing()),
            Bullet()
        )
    ),
    ("primary_key_definition",
     Then(
         Bullet(),
         text("PRIMARY"),
         text("KEY"),
         text("("),
         Loop(production("<field name>"), text(",")),
         text(")"),
         Bullet()
     )
     ),
    ("foreign_key_definition",
     Then(
         Bullet(),
         text("FOREIGN"),
         text("KEY"),
         text("("),
         Loop(production("<field name>"), text(",")),
         text(")"),
         text("REFERENCES"),
         production("table_ref"),
         text("("),
         Loop(production("<field name>"), text(",")),
         text(")"),
         production("fk_rules"),
         Bullet()
     )
     ),
    ("add_foreign_key",
     Then(
         Bullet(),
         text("ALTER"),
         text("TABLE"),
         production("<table name>"),
         text("ADD"),
         text("CONSTRAINT"),
         production("<fk name>"),
         production("foreign_key_definition"),
         Bullet()
     )
     ),
    ("create_index",
     Then(
         Bullet(),
         text("CREATE"),
         text("INDEX"),
         production("<index name>"),
         text("ON"),
         production("<table name>"),
         text("("),
         Loop(production("<field name>"), text(",")),
         text(")"),
         Bullet()
     )
     ),
    ("create_view",
     Then(
         Bullet(),
         text("CREATE"),
         text("VIEW"),
         production("<view name>"),
         text("AS"),
         production("query"),
         Bullet()
     )
     ),
    ("query",
     Then(
         Bullet(),
         text("SELECT"),
         Or(text("DISTINCT"), Nothing()),
         Loop(
             Or(
                 Then(production("term"),
                      Or(Then(text("AS"), production("<field alias>")), Nothing())),
                 Then(production("aggregate"))
             ),
             text(",")),
         text("FROM"),
         production("from_clause"),
         Or(Then(text("WHERE"), production("condition")), Nothing()),
         Or(Then(production("group_by")), Nothing()),
         Bullet()
     )
     ),
    ("from_clause",
     Then(
         Bullet(),
         Then(production("table_ref"), Or(Then(text("AS"), production("<table alias>")), Nothing())),
         Or(
             Loop(Then(Or(text("INNER"), text("LEFT"), text("RIGHT")),
                       text("JOIN"),
                       production("table_ref"),
                       Or(Then(text("AS"), production("<table alias>")), Nothing()),
                       text("ON"),
                       production("condition")),
                  Nothing()
                  ),
             Nothing()
         ),
         Bullet()
     )
     ),
    ("term",
     Then(
         Bullet(),
         Loop(
             Then(Or(text("-"), Nothing()), Or(
                 production("primary_term"),
                 Then(text("("), production("term"), text(")")))),
             Or(text("+"), text("-"), text("*"), text("/"), text("||"))
         ),
         Bullet()
     )
     ),
    ("primary_term",
     Then(
         Bullet(),
         Or(
             Then(Or(Then(Or(production("<table name>"), production("<table alias>")), text(".")), Nothing()),
                  production("<field name>")),
             production("<text literal>"),
             production("<integer literal>"),
             production("<float.-point literal>"),
             production("TRUE"),
             production("FALSE"),
             production("GETDATE()"),
             production("<param_literal>")
         ),
         Bullet()
     )
     ),
    ("condition",
     Then(
         Bullet(),
         Loop(
             Then(Or(text("NOT"), Nothing()),
                  Or(production("predicate"),
                     Then(text("("), production("condition"), text(")")))),
             Or(text("AND"), text("OR")),
         ),
         Bullet()
     )
     ),
    ("predicate",
     Then(
         Bullet(),
         production("term"),
         Or(
             Then(Or(text("="), text(">"), text(">="), text("<="), text("<"), text("<>"), text("LIKE")),
                  production("term")),
             Then(text("BETWEEN"), production("term"), text("AND"), production("term")),
             Then(text("IN"), text("("), Loop(production("term"), text(",")), text(")")),
             Then(text("IS"), text("NULL"))
         ),
         Bullet()
     )
     ),
    ("aggregate",
     Then(
         Bullet(),
         Or(
             Then(text("COUNT"), text("("), text("*"), text(")")),
             Then(
                 Or(
                     Then(text("SUM")),
                     Then(text("MIN")),
                     Then(text("MAX"))
                 ),
                 Then(text("("), production("term"), text(")"))
             )
         ),
         Then(text("AS"), production("<field alias>")),
         Bullet()
     )
     ),
    ("materialized_aggregate",
     Then(
         Bullet(),
         Or(
             Then(text("COUNT"), text("("), text("*"), text(")")),
             Then(
                 Then(text("SUM"), text("("), production("<field name>"), text(")"))
             )
         ),
         Then(text("AS"), production("<field alias>")),
         Bullet()
     )
     ),
    ("group_by",
     Then(
         Bullet(),
         text("GROUP"), text("BY"),
         Loop(
             Or(
                 Then(production("<field name>")),
                 Then(production("<field alias>"))
             ),
             text(",")
         ),
         Bullet()
     )
     ),
    ("create_materialized_view",
     Then(
         Bullet(),
         text("CREATE"),
         text("MATERIALIZED"),
         text("VIEW"),
         production("<view name>"),
         text("AS"),
         text("SELECT"),
         Loop(
             Or(
                 Then(text(","), production("materialized_aggregate")),
                 Then(text(","), production("<field name>"), Or(
                     Then(text("AS"), production("<field alias>")),
                     Nothing()
                 ))
             ),
             text(",")
         ),
         text("FROM"),
         production("table_ref"),
         Then(production("group_by")),
         Bullet()
     )
     ),
    ("create_function",
     Then(
         Bullet(),
         text("CREATE"),
         text("FUNCTION"),
         production("<function name>"),
         text("("),
         Loop(
             production("param_definition"),
             text(",")
         ),
         text(")"),
         text("AS"),
         production("query"),
         Bullet()
     )
     ),
    (
        "param_definition",
        Then(
            Bullet(),
            production("<param name>"),
            Or(
                text("INT"),
                text("REAL"),
                text("DECIMAL"),
                text("VARCHAR"),
                text("DATETIME"),
                text("BIT")
            ),
            Bullet()
        )
    ),
    (
        "param_literal",
        Then(
            Bullet(),
            text('$'),
            production("<param name>"),
            Bullet()
        )
    )

])

options = {
    "raildraw_title_before": 20,
    "raildraw_title_after": 30,
    "raildraw_scale": 2
}

i = 0
for pname in productions.keys():
    i += 1
    draw_to_png(OrderedDict([(pname, productions[pname])]), options, 'target/celestasql/' +
                ('0' if i < 10 else '') + str(i) + '.' + pname + '.png', True)
