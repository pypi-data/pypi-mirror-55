# _*_ coding: utf-8 _*_
import enum


__author__ = "Md Nazrul Islam<email2nazrul@gmail.com>"


class FHIR_VERSION(enum.Enum):
    """ """

    DEFAULT = "R4"
    STU3 = "STU3"
    R4 = "R4"
    DSTU2 = "DSTU2"


@enum.unique
class SortOrderType(enum.Enum):
    """ """

    ASC = "asc"
    DESC = "desc"


@enum.unique
class MatchType(enum.Enum):
    """ """

    ANY = "ANY"
    ALL = "ALL"
    ONE = "ONE"
    NONE = "NONE"


@enum.unique
class TermMatchType(enum.Enum):
    """ """

    EXACT = "EXACT"
    STARTWITH = "STARTWITH"
    ENDWITH = "ENDWITH"
    FULLTEXT = "FULLTEXT"


@enum.unique
class GroupType(enum.Enum):
    DECOUPLED = "DECOUPLED"
    COUPLED = "COUPLED"


@enum.unique
class WhereConstraintType(enum.Enum):
    """ """

    # normal key, value conditional
    T1 = "T1"
    # constraint certain FHIR Resource type
    T2 = "T2"
    # complex constraint with subpath
    T3 = "T3"


@enum.unique
class EngineQueryType(enum.Enum):
    """" """
    DDL = "DDL"
    DML = "DML"
    COUNT = "COUNT"
