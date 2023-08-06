import logging
import re
import traceback
from typing import List
from elasticsearch_dsl import Search
from elasticsearch_dsl.query import (
    QueryString,
    Bool,
    Match,
    SpanNear,
    SpanMulti,
    SpanFirst,
    SpanTerm,
    SpanOr,
)

from tiidan_utils.util import log_function
from .data import _Data

data = _Data()
log = logging.getLogger(__name__)


@log_function(log)
def get_supplier_query(name, field="Exporter"):
    return Search().query(parse_structure(name).get_query(field)).to_dict()


class Replacer:
    def __init__(self, pattern, query):
        self.pattern = pattern
        self.query = query


class _Fuzzy(Match):
    def __init__(self, term, field):
        super().__init__(**{field: dict(fuzziness="AUTO", query=term, prefix_length=1)})


class _QueryString(QueryString):
    def __init__(self, query, field):
        super().__init__(default_field=field, query=query)


class _SpanMultiFuzzy(SpanMulti):
    def __init__(self, query, field):
        super().__init__(
            match={
                "fuzzy": {
                    field: {"value": query, "fuzziness": "AUTO", "prefix_length": 1}
                }
            }
        )


def regexes(field):
    return [
        Replacer(r"\bproducts?\b", _Fuzzy("product", field)),
        Replacer(r"\bim?p?o?r?t?\s*ex?p?o?r?t?\b", _QueryString("i* e*", field)),
        Replacer(r"\s+xing\b", _QueryString("*xing", field)),
        Replacer(r"\s+lumin\b", _QueryString("*lumin", field)),
        Replacer(
            r"\bindustry?i.?a?l?\b", _QueryString("industrial~ OR industry~", field)
        ),
        Replacer(r"\bcompany\b", _QueryString("-company", field)),
        Replacer(r"\beconomy?i?c?\b", _QueryString("economy~ OR economic~", field)),
        Replacer(r"\binstru?m?e?n?t?s?a?l?\b", _QueryString("istru*", field)),
        Replacer(r"\btrade?(ing)?\b", _QueryString("trade~ OR trading~", field)),
    ]


def clean_name(name):
    regexes = [
        {"pattern": r"[\[\]()\\ /:;\'.,`-]"},
        {"pattern": r"\n"},
        {"pattern": r"co\s*ltd?"},
        {"pattern": r"(limited)|(\blt?d?)|(llc)\b"},
        {"pattern": r"\bcor?p?o?r?a?t?i?o?n?\b"},
        {"pattern": r"\binco?r?p?o?r?a?t?e?d?\b"},
        {"pattern": r"\bsha\b"},
        {"pattern": r"\bbldg\b"},
        {"pattern": r"\band\b"},
        {"pattern": r"&"},
        {"pattern": r"\bgmbh\b"},
        {"pattern": r"\bno\b"},
        {"pattern": r"\s+"},
    ]
    trade_search = name.lower()
    for r in regexes:
        trade_search = re.sub(r["pattern"], r.get("replace", " "), trade_search)
    return trade_search.strip()


def get_type_query(tokens, field):
    regexes = {
        r"li?m?i?te?d": lambda x: SpanOr(
            clauses=[_SpanMultiFuzzy("limited", field), _SpanMultiFuzzy("ltd", field)]
        ),
        "cor?p?o??r?a?t?i?o?n?": lambda x: SpanOr(
            clauses=[
                _SpanMultiFuzzy("corp", field),
                _SpanMultiFuzzy("co", field),
                _SpanMultiFuzzy("corporation", field),
            ]
        ),
        "default": lambda x: _SpanMultiFuzzy(x, field),
    }
    clauses = []
    for token in tokens:
        for reg, term in regexes.items():
            if re.search(reg, token):
                clauses.append(term(token))
                break
        else:
            clauses.append(regexes["default"](token))
    return SpanNear(clauses=clauses, in_order=True, slop=0)


class ChineseCompany:
    pass


class DomesticChineseCompany:
    def __init__(self, tokens):
        self.location = tokens[0]
        log.debug(f"location: {self.location}")
        tokens = tokens[1:]
        type_index = self.get_type_index(tokens)
        self.type = []
        if type_index:
            self.type = tokens[type_index : type_index + 2]
            log.debug(f"type: {', '.join(self.type)}")
            self.rest = tokens[:type_index]
        else:
            self.rest = tokens[:]
        log.debug(f"rest: {', '.join(self.rest)}")

    @staticmethod
    def get_type_index(tokens: List[str]) -> int:
        for i, t in enumerate(tokens):
            if t == "co" and (
                i + 1 == len(tokens)
                or re.match(
                    r"\b((ltd?)|(inco?r?p?o?r?a?t?ed?)"
                    r"|(llc)|(limited)|(liability)|(company)"
                    r"|(LIMITED))\b",
                    tokens[i + 1],
                )
            ):
                return i
            if re.match(
                r"\b((corpo?r?a?t?i?o?n?)|(ltd?)|(inco?r?p?o?r?a?t?ed?)"
                r"|(llc)|(limited)|(liability)|(company)"
                r"|(LIMITED))\b",
                t,
            ):
                return i
        return None

    def get_query(self, field="Exporter"):
        if len(self.rest) == 0:
            return None
        else:
            clauses = [SpanTerm(**{field: self.location})] + [
                _SpanMultiFuzzy(x, field) for x in self.rest
            ]
            if len(self.type):
                clauses.append(get_type_query(self.type, field))

            return Bool(
                must=[
                    SpanFirst(match=SpanTerm(**{field: self.location}), end=1),
                    SpanNear(clauses=clauses, in_order=True, slop=0),
                ]
            )


class ForeignOwnedChineseCompany:
    pass


class NationallyOwnedChineseCompany:
    pass


class UncategorizedChineseCompany:
    def __init__(self, tokens):
        self.tokens = tokens

    def get_query(self, field="Exporter"):
        return get_type_query(self.tokens, field)


def tokenize(name: str) -> List[str]:
    name = re.sub(r"[\[\]()\\ /:;\'.,`\-\"\}&]", " ", name)
    name = re.sub(r"\s+", " ", name)
    name = name.strip()
    return [x.lower() for x in name.split(" ")]


def parse_structure(name):
    tokens = tokenize(name)
    for i, t in enumerate(tokens):
        if i == 0 and (t in data.china_provinces or t in data.china_cities):
            try:
                return DomesticChineseCompany(tokens)
            except Exception as e:
                log.warning(traceback.format_exc())
                log.warning(f"couldn't parse name: {name}")
    return UncategorizedChineseCompany(tokens)
