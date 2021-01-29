Version 0.5.0
=============

Released 2021-01-29

- Drop support for Python < 3.8, add support for Python >= 3.8


Version 0.4.0
=============

Released 2018-04-02

- Fix usage with application factory pattern
- Resolve the logging instance at first access instead of keeping a reference
  to a proxy object
- Add ``get_effective_level`` and ``set_level`` to set and get the
  logging level respectively


Version 0.3.1
=============

Released 2016-03-14

- Fix usage with application factory pattern (*Backported from 0.4.0*)


Version 0.3.0
=============

Released 2016-03-08

- Replace Henson's logger with the instance of ``Logging``


Version 0.2.0
=============

Released 2015-11-19

- Add support for log handler kwargs (*Note: this change drops support for
  Python 3.4 and requires 3.5+*)
- Add support for ``LOG_FORMATTER`` setting to control the formatter used by
  the henson log handler


Version 0.1.0
=============

Released 2015-11-03

- Initial release
