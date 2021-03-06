Changelog
=========

1.1.0
-----

-  Simplify dev environment configuration.
-  Add tox configuration for locally testing against multiple python versions.
-  Fix a bug in the nosetests helper implementation that was making it
   ignore passed in configuration.
-  Fix a bug that causing testtube to choke on simple method based tests.
-  Add an ``IGNORE_PATTERNS`` configuration option which supersedes test group
   pattern matches and allows users to configure testtube to always ignore
   certain files.
-  Add integration tests.
-  Factor out threading anti-patterns from core (``time.sleep()``).

1.0.0
-----

-  Make tests configurable
-  Make test groups configurable
-  Centralizes output in a renderer object
-  Adds support for audible bells
-  Adds test group fail fast support (aborts test run)
-  Adds test fail fast support (aborts test group)
-  Adds helper base class to make writing tests easier
-  Adds a frosted helper
-  Rewrite of configuration handling
-  Eliminates redundant helpers: pep8\_all, pyflakes\_all,
   nosetests\_all

0.2.0
-----

-  Added python 3 support

0.0.1
-----

-  Initial release
