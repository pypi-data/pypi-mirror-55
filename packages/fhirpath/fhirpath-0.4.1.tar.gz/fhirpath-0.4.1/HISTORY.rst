=======
History
=======

0.4.1 (2019-11-05)
------------------

Bugfixes

- ``fhirpath.search.Search.parse_query_string`` now returning ``MuliDict``(what is expected) instead of ``MultiDictProxy``.


0.4.0 (2019-10-24)
------------------

Improvements

- Now full ``select`` features are accepted, meaning that you can provide multiple path in ``select`` section. for example ``select(Patient.name, Patient.gender)``.

- FHIRPath ``count()`` and ``empty()`` functions are supported.

- Supports path navigation with index and functions inside ``select``. Example ``[index]``, ``last()``, ``first()``, ``Skip()``, ``Take()``, ``count()``.

Breakings

- ``QueryResult.first`` and ``QueryResult.single`` are no longer return FHIR Model instance instead returning ``fhirpath.engine.EngineResultRow``.

- ``QueryResult.fetchall`` returning list of ``fhirpath.engine.EngineResultRow`` instead of FHIR JSON.

- ``QueryResult`` iteration returning list of FHIR Model instance on condition (if select is `*`), other than returning list of ``fhirpath.engine.EngineResultRow``.


0.3.1 (2019-10-08)
------------------

Improvements

- Add support for search parameter expression that contains with space+as (``MedicationRequest.medication as CodeableConcept``)

Bugfixes

- ``not`` modifier is now working for ``Coding`` and ``CodeableConcept``.

- "ignore_unmapped" now always True in case of nested query.

- "unmapped_type" now set explicitly long value. See related issue https://stackoverflow.com/questions/17051709/no-mapping-found-for-field-in-order-to-sort-on-in-elasticsearch


0.3.0 (2019-09-30)
------------------

Improvements

- Supports multiple AND values for same search parameter!.

- Add support FHIR version ``STU3`` compability for Money type search.[nazrulworld]

- IN Query support added.[nazrulworld]

- Support PathElement that contains string path with .as(), thus suports for Search also.

- Supports ``Duration`` type in Search.

- Add support ``composite`` type search param.


Bugfixes

- Multiple search values (IN search)

- Missing ``text`` for HumanName and Address search.



0.2.0 (2019-09-15)
------------------

Breakings:

- Built-in providers ( ``guillotina_app`` and ``plone_app`` ) have been wiped as both becoming separate pypi project.

- ``queries`` module has been moved from ``fql`` sub-package to fhirpath package and also renamed as ``query``.


Improvements:

- There are so many improvements made for almost all most modules.

- FhirSearch coverages are increased.

- Sort, Limit facilities added in Query as well in FhirSearch.


Bugfixes:

- numbers of bugs fixed.



0.1.1 (2019-08-15)
------------------

- First working version has been released. Of-course not full featured.


0.1.0 (2018-12-15)
------------------

* First release on PyPI.(Just register purpose, not usable at all, next release coming soon)
