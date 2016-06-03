from termcolor import colored

from .base import IntegrationTest, SAMPLE_PROJECT


class WelcomeMessageTest(IntegrationTest):
    def test_output_on_startup(self):
        self.assertIn(
            'testtube is now watching %s for changes...' % SAMPLE_PROJECT,
            self.output_accumulator.wait('testtube is now'))


class RuleMatchTest(IntegrationTest):
    def setUp(self):
        super(RuleMatchTest, self).setUp()

        self.touch('file.py')

        self.output = self.output_accumulator.wait('Test group 1:')

    def test_outputs_test_report(self):
        self.assertIn('Test Report', self.output)

    def test_executes_corresponding_tests_when_rule_matches(self):
        self.assertIn(
            'Test group 1:	%s' % colored('Flake8', 'green'),
            self.output)


class SimpleMethodTestsTest(IntegrationTest):
    def setUp(self):
        super(SimpleMethodTestsTest, self).setUp()

        self.touch('foo.bar')

        self.output = self.output_accumulator.wait('simple_method_test')

    def test_are_executed_when_their_test_group_matches(self):
        self.assertIn(
            'Test group 1:	%s' % colored('simple_method_test', 'green'),
            self.output)
