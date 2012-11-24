# Fail Fast Feature
Users should be able to configure a test tuple so that it "fails fast" (as
soon as one of the tests in the tuple fails, the entire set stops running for
that iteration).

* `PATTERNS` should allow a third tuple value (a dictionary) to be used for
configuring that set of tests.
* Helpers should be modified to return a boolean indicating success or failure
* runner.py should be modified to respect the `fail_fast` configuration option
* Helpers should be modified so that they always expect to be passed that
optional configuration dictionary? This is unnecessary to achieve this feature
but might be something that will be needed later? (If this is done, be sure to
update the docs)