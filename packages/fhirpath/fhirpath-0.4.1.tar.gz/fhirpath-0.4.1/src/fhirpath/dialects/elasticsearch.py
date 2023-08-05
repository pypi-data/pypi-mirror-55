# _*_ coding: utf-8 _*_
"""ElasticSearch Dialect"""
import logging
import operator
import re

import isodate
from zope.interface import alsoProvides

from fhirpath.enums import GroupType
from fhirpath.enums import MatchType
from fhirpath.enums import SortOrderType
from fhirpath.enums import TermMatchType
from fhirpath.interfaces import IFhirPrimitiveType
from fhirpath.interfaces import IPrimitiveTypeCollection
from fhirpath.interfaces.dialects import IIgnoreNestedCheck
from fhirpath.interfaces.fql import IExistsTerm
from fhirpath.interfaces.fql import IGroupTerm
from fhirpath.interfaces.fql import IInTerm
from fhirpath.interfaces.fql import INonFhirTerm
from fhirpath.interfaces.fql import ITerm

from .base import DialectBase


__author__ = "Md Nazrul Islam<email2nazrul@gmail.com>"
logger = logging.getLogger("fhirpath.dialects.elasticsearch")
URI_SCHEME = re.compile(r"^https?://", re.I)
ES_PY_OPERATOR_MAP = {
    operator.eq: None,
    operator.ne: None,
    operator.gt: "gt",
    operator.lt: "lt",
    operator.ge: "gte",
    operator.le: "lte",
}


class ElasticSearchDialect(DialectBase):
    """ """

    def _apply_nested(self, query, dotted_path):
        """ """
        wrapper = {
            "nested": {
                "path": dotted_path,
                "query": query,
                "ignore_unmapped": True,
                "score_mode": "min",
            }
        }
        return wrapper

    def _apply_path_replacement(self, dotted_path, root_replacer):
        """ """
        if root_replacer is not None:
            path_ = ".".join([root_replacer] + list(dotted_path.split(".")[1:]))
        else:
            path_ = dotted_path
        return path_

    def _attach_nested_on_demand(self, context, query_, root_replacer):
        """ """
        path_context = context
        qr = query_

        while True:
            if path_context.multiple and not IFhirPrimitiveType.implementedBy(
                path_context.type_class
            ):
                path_ = self._apply_path_replacement(
                    str(path_context._path), root_replacer
                )
                qr = self._apply_nested(qr, path_)
            if path_context.is_root():
                break
            path_context = path_context.parent

        return qr

    def _create_term(self, path, value, multiple=False):
        """Create ES Query term"""
        multiple_ = isinstance(value, (list, tuple)) or multiple is True
        if multiple_ is True and not isinstance(value, (list, tuple)):
            value = [value]

        if multiple_:
            q = {"terms": {path: value}}
        else:
            q = {"term": {path: value}}

        return q

    def _create_dotted_path(self, term, root_replacer=None):
        """ """
        if INonFhirTerm.providedBy(term):
            return term.path

        if root_replacer is not None:
            path_ = ".".join([root_replacer] + list(term.path.path.split(".")[1:]))
        else:
            path_ = term.path.path
        return path_

    def _clean_up(self, body_structure):
        """ """
        if len(body_structure["query"]["bool"]["should"]) == 0:
            del body_structure["query"]["bool"]["should"]

        if len(body_structure["query"]["bool"]["must"]) == 0:
            del body_structure["query"]["bool"]["must"]

        if len(body_structure["query"]["bool"]["must_not"]) == 0:
            del body_structure["query"]["bool"]["must_not"]

        if len(body_structure["query"]["bool"]["filter"]) == 0:
            del body_structure["query"]["bool"]["filter"]

        if len(body_structure["sort"]) == 0:
            del body_structure["sort"]

        if body_structure["_source"] is not False:

            if len(body_structure["_source"]["includes"]) == 0:
                del body_structure["_source"]["includes"]

            if len(body_structure["_source"]["excludes"]) == 0:
                del body_structure["_source"]["excludes"]

            if len(body_structure["_source"]) == 0:
                del body_structure["_source"]

    def _get_path_mapping_info(self, mapping, dotted_path):
        """ """
        mapping_ = mapping["properties"]

        for path_ in dotted_path.split(".")[1:]:
            try:
                info_ = mapping_[path_]
            except KeyError:
                logger.warn("No mapping found for {0}".format(dotted_path))
                return {}
            if "properties" in info_:
                mapping_ = info_["properties"]
            else:
                return info_

    def compile(self, query, mapping, root_replacer=None):
        """
        :param: query

        :param: mapping: Elasticsearch mapping for FHIR resources.

        :root_replacer: Path´s root replacer:
            Could be mapping name or index name in zope´s ZCatalog context
        """
        body_structure = self.create_structure()
        conditional_terms = query.get_where()

        for term in conditional_terms:
            """ """
            q, unary_operator = self.resolve_term(term, mapping, root_replacer)

            if unary_operator == operator.neg:
                container = body_structure["query"]["bool"]["must_not"]
            elif unary_operator == operator.pos:
                container = body_structure["query"]["bool"]["filter"]
            else:
                # xxx: if None may be should?
                from inspect import currentframe, getframeinfo

                frameinfo = getframeinfo(currentframe())
                raise NotImplementedError(
                    "File: {0} Line: {1}".format(
                        frameinfo.filename, frameinfo.lineno + 1
                    )
                )

            container.append(q)

        # ResourceType bind
        self.apply_from_constraint(query, body_structure, root_replacer=root_replacer)
        # Sorting
        self.apply_sort(query.get_sort(), body_structure, root_replacer=root_replacer)
        # Limit
        self.apply_limit(query.get_limit(), body_structure)
        # ES source_
        self.apply_source_filter(query, body_structure, root_replacer=root_replacer)

        self._clean_up(body_structure)

        if "should" in body_structure["query"]["bool"]:
            if "minimum_should_match" not in body_structure["query"]["bool"]:
                body_structure["query"]["bool"]["minimum_should_match"] = 1

        return body_structure

    def resolve_term(self, term, mapping, root_replacer):
        """ """
        if IGroupTerm.providedBy(term):
            unary_operator = operator.pos
            if term.type == GroupType.DECOUPLED:

                if term.match_operator == MatchType.ANY:
                    qr = {"bool": {"should": list()}}
                    container = qr["bool"]["should"]
                    qr["bool"]["minimum_should_match"] = 1

                elif term.match_operator == MatchType.ALL:
                    qr = {"bool": {"filter": list()}}
                    container = qr["bool"]["filter"]

                elif term.match_operator == MatchType.NONE:
                    qr = {"bool": {"must_not": list()}}
                    container = qr["bool"]["must_not"]

                alsoProvides(term, IIgnoreNestedCheck)

            elif term.type == GroupType.COUPLED:
                if term.match_operator == MatchType.NONE:
                    qr = {"bool": {"must_not": list()}}
                    container = qr["bool"]["must_not"]
                else:
                    qr = {"bool": {"filter": list()}}
                    container = qr["bool"]["filter"]
            else:
                raise NotImplementedError

            for t_ in term.terms:
                # single term resolver should not look at this
                if term.type == GroupType.COUPLED:
                    alsoProvides(t_, IIgnoreNestedCheck)

                resolved = self.resolve_term(t_, mapping, root_replacer)
                container.append(resolved[0])

            if not IIgnoreNestedCheck.providedBy(term):
                qr = self._attach_nested_on_demand(term.path.context, qr, root_replacer)

            return qr, unary_operator

        elif IInTerm.providedBy(term):

            unary_operator = term.unary_operator
            qr = {"bool": {"should": list()}}
            container = qr["bool"]["should"]

            for t_ in term:
                resolved = self.resolve_term(t_, mapping, root_replacer)
                container.append(resolved[0])
            if len(container) > 0:
                qr["bool"]["minimum_should_match"] = 1
            return qr, unary_operator

        elif IExistsTerm.providedBy(term):
            return self.resolve_exists_term(term, root_replacer=root_replacer)

        elif ITerm.providedBy(term):

            if IFhirPrimitiveType.implementedBy(term.path.context.type_class):

                if term.path.context.type_name in (
                    "string",
                    "uri",
                    "url",
                    "canonical",
                    "code",
                    "oid",
                    "id",
                    "uuid",
                    "boolean",
                ):
                    # xxx: may do something special?
                    multiple = term.path.context.multiple
                    dotted_path = self._create_dotted_path(term, root_replacer)
                    value = term.get_real_value()

                    map_info = self._get_path_mapping_info(mapping, dotted_path)

                    if map_info.get("type", None) == "text":
                        resolved = self.resolve_string_term(
                            term, map_info, root_replacer
                        )

                    else:
                        q = self._create_term(dotted_path, value, multiple=multiple)
                        resolved = q, term.unary_operator

                elif term.path.context.type_name in (
                    "dateTime",
                    "date",
                    "time",
                    "instant",
                ):

                    resolved = self.resolve_datetime_term(term, root_replacer)

                elif term.path.context.type_name in (
                    "integer",
                    "decimal",
                    "unsignedInt",
                    "positiveInt",
                ):

                    resolved = self.resolve_numeric_term(term, root_replacer)
                else:
                    raise NotImplementedError

                if IIgnoreNestedCheck.providedBy(term):
                    return resolved

                # check for nested
                qr, unary_operator = resolved
                qr = self._attach_nested_on_demand(term.path.context, qr, root_replacer)
                return qr, unary_operator
            else:
                raise NotImplementedError("Line 288")

        elif INonFhirTerm.providedBy(term):
            assert IFhirPrimitiveType.providedBy(term.value)
            return self.resolve_nonfhir_term(term)

    def resolve_datetime_term(self, term, root_replacer=None):
        """TODO: 1.) Value Conversion(stringify) based of context.type_name
        i.e date or dateTime or Time """
        qr = dict()
        if INonFhirTerm.providedBy(term):
            type_name = term.value.__visit_name__
        else:
            type_name = term.path.context.type_name

        value = term.get_real_value()
        path_ = self._create_dotted_path(term, root_replacer)

        if type_name in ("dateTime", "instant"):
            value_formatter = (
                isodate.DATE_EXT_COMPLETE + "T" + isodate.TIME_EXT_COMPLETE
            )
        elif type_name == "date":
            value_formatter = isodate.DATE_EXT_COMPLETE
        elif type_name == "time":
            value_formatter = isodate.TIME_EXT_COMPLETE
        else:
            raise NotImplementedError

        if term.comparison_operator in (operator.eq, operator.ne):
            qr["range"] = {
                path_: {
                    ES_PY_OPERATOR_MAP[operator.ge]: isodate.strftime(
                        value, value_formatter
                    ),
                    ES_PY_OPERATOR_MAP[operator.le]: isodate.strftime(
                        value, value_formatter
                    ),
                }
            }

        elif term.comparison_operator in (
            operator.le,
            operator.lt,
            operator.ge,
            operator.gt,
        ):
            qr["range"] = {
                path_: {
                    ES_PY_OPERATOR_MAP[term.comparison_operator]: isodate.strftime(
                        value, value_formatter
                    )
                }
            }

        if type_name in ("dateTime", "instant", "time") and value.tzinfo:
            timezone = isodate.tz_isoformat(value)
            if timezone not in ("", "Z"):
                qr["range"][path_]["time_zone"] = timezone

        if (
            term.comparison_operator != operator.ne
            and term.unary_operator == operator.neg
        ) or (
            term.comparison_operator == operator.ne
            and term.unary_operator != operator.neg
        ):
            unary_operator = operator.neg
        else:
            unary_operator = operator.pos

        return qr, unary_operator

    def resolve_numeric_term(self, term, root_replacer=None):
        """ """
        qr = dict()
        path_ = self._create_dotted_path(term, root_replacer)
        value = term.get_real_value()

        if term.comparison_operator in (operator.eq, operator.ne):
            qr["range"] = {
                path_: {
                    ES_PY_OPERATOR_MAP[operator.ge]: value,
                    ES_PY_OPERATOR_MAP[operator.le]: value,
                }
            }

        elif term.comparison_operator in (
            operator.le,
            operator.lt,
            operator.ge,
            operator.gt,
        ):
            qr["range"] = {path_: {ES_PY_OPERATOR_MAP[term.comparison_operator]: value}}

        if (
            term.comparison_operator != operator.ne
            and term.unary_operator == operator.neg
        ) or (
            term.comparison_operator == operator.ne
            and term.unary_operator != operator.neg
        ):
            unary_operator = operator.neg
        else:
            unary_operator = operator.pos

        return qr, unary_operator

    def resolve_string_term(self, term, map_info, root_replacer=None):
        """ """
        # xxx: could have support for free text search
        path_ = self._create_dotted_path(term, root_replacer)

        fulltext_analyzers = ("standard",)
        value = term.get_real_value()
        if map_info.get("analyzer", "standard") in fulltext_analyzers:
            # xxx: should handle exact match
            if term.match_type == TermMatchType.EXACT:
                qr = {"match_phrase": {path_: value}}
            else:
                qr = {"match": {path_: value}}
        elif ("/" in value or URI_SCHEME.match(value)) and ".reference" in path_:
            qr = {"match_phrase": {path_: value}}
        else:
            qr = self._create_term(path_, value, term.path.context.multiple)

        resolved = qr, term.unary_operator
        return resolved

    def resolve_exists_term(self, term, root_replacer=None):
        """ """
        path_ = self._create_dotted_path(term, root_replacer)

        qr = {"exists": {"field": path_}}
        if not INonFhirTerm.providedBy(term):
            qr = self._attach_nested_on_demand(term.path.context, qr, root_replacer)

        return qr, term.unary_operator

    def resolve_nonfhir_term(self, term):
        """ """
        if IPrimitiveTypeCollection.providedBy(term.value):
            visit_name = term.value.registered_visit
            if visit_name in ("string", "code", "oid", "id", "uuid"):
                if visit_name == "string" and term.match_type not in (
                    None,
                    TermMatchType.EXACT,
                ):
                    raise ValueError(
                        "PrimitiveTypeCollection instance is not "
                        "allowed if match type not exact"
                    )
            else:
                raise NotImplementedError
        else:
            visit_name = term.value.__visit_name__

        if visit_name in (
            "string",
            "uri",
            "url",
            "canonical",
            "code",
            "oid",
            "id",
            "uuid",
            "boolean",
        ):
            if term.match_type not in (TermMatchType.FULLTEXT, None):
                resolved = self.resolve_string_term(term, {}, None)
            else:
                value = term.get_real_value()
                q = self._create_term(term.path, value)
                resolved = q, term.unary_operator

        elif visit_name in ("dateTime", "date", "time", "instant"):

            resolved = self.resolve_datetime_term(term, None)

        elif visit_name in ("integer", "decimal", "unsignedInt", "positiveInt"):

            resolved = self.resolve_numeric_term(term, None)
        else:
            raise NotImplementedError
        return resolved

    def apply_limit(self, limit_clause, body_structure):
        """ """
        if limit_clause.empty:
            # no limit! should be scroll
            body_structure["scroll"] = "1m"
            return
        if isinstance(limit_clause.limit, int):
            body_structure["size"] = limit_clause.limit
        if isinstance(limit_clause.offset, int):
            body_structure["from"] = limit_clause.offset

    def apply_sort(self, sort_terms, body_structure, root_replacer=None):
        """ """
        for term in sort_terms:
            if root_replacer is not None:
                path_ = ".".join([root_replacer] + list(term.path.path.split(".")[1:]))
            else:
                path_ = term.path.path
            item = {
                # https://www.elastic.co/guide/en/elasticsearch/\
                # reference/current/search-request-body.html#_ignoring_unmapped_fields
                path_: {
                    "order": term.order == SortOrderType.DESC and "desc" or "asc",
                    "unmapped_type": "long",
                }
            }
            body_structure["sort"].append(item)

    def apply_from_constraint(self, query, body_structure, root_replacer=None):
        """We force apply resource type boundary"""
        for res_name, res_klass in query.get_from():
            path_ = "{0}.resourceType".format(root_replacer or res_name)
            term = {"term": {path_: res_name}}
            body_structure["query"]["bool"]["filter"].append(term)

    def apply_source_filter(self, query, body_structure, root_replacer=None):
        """https://www.elastic.co/guide/en/elasticsearch/reference/\
        current/search-request-body.html#request-body-search-source-filtering

            1.) we are using FHIR field data from ES server directly, unlike collective.
                elasticsearch, where only path is retrieve, then using that set
                zcatalog brain, this patternt might good for
                general puporse but here we exclusively need fhir
                resource only which is already stored in ES.
                Our approach will be definately performance optimized!

            2.) We might loose minor security (only zope specific),
                because here permission is not checking while getting full object.
        """

        if len(query.get_select()) == 0:
            # No select no source!
            body_structure["_source"] = False
            return

        def replace(path_el):
            if root_replacer is None or path_el.non_fhir:
                return path_el.path
            parts = path_el.path.split(".")
            if len(parts) > 1:
                return ".".join([root_replacer] + list(parts[1:]))
            else:
                return root_replacer

        includes = list()
        if len(query.get_select()) == 1 and query.get_select()[0].star:
            if root_replacer is None:
                includes.append(query.get_from()[0][0])
            else:
                includes.append(root_replacer)
        elif len(query.get_select()) > 0:
            for path_el in query.get_select():
                includes.append(replace(path_el))

        if len(includes) > 0:
            body_structure["_source"]["includes"].extend(includes)

    def create_structure(self):
        """ """
        return {
            "query": {
                "bool": {
                    "should": list(),
                    "must": list(),
                    "must_not": list(),
                    "filter": list(),
                }
            },
            "size": 100,
            "from": 0,
            "sort": list(),
            "_source": {"includes": [], "excludes": []},
        }
