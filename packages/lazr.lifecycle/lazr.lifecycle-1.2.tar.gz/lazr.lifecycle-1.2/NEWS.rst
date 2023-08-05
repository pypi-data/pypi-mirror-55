=======================
NEWS for lazr.lifecycle
=======================

1.2 (2019-11-04)
================

- Import IObjectEvent from zope.interface rather than zope.component.
- Add ObjectModifiedEvent.descriptions property, for compatibility with
  zope.lifecycleevent >= 4.2.0.
- Switch from buildout to tox.
- Add Python 3 support.

1.1 (2009-12-03)
================

- Add IDoNotSnapshot and doNotSnapshot to allow the exclusion of
  certain fields.

1.0 (2009-08-31)
================

- Remove build dependencies on bzr and egg_info

- remove sys.path hack in setup.py for __version__

0.1 (2009-03-24)
================

- Initial release
