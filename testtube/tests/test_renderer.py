import sys

from . import call, Mock, patch, unittest

from termcolor import colored

from testtube.renderer import Renderer


class RendererTest(unittest.TestCase):
    def setUp(self):
        # use self.actual_stdout.write() for debugging. Print won't work
        # while the unit is under test as a resut of the stdout patching
        # below.
        self.actual_stdout = sys.stdout

        stdout_patch = patch('sys.stdout')
        self.stdout = stdout_patch.start()
        self.addCleanup(stdout_patch.stop)

        self.renderer = Renderer()


class RendererNotice(RendererTest):
    def setUp(self):
        super(RendererNotice, self).setUp()
        self.renderer.notice('yay')

    def test_prints_passed_message(self):
        self.stdout.write.assert_has_calls([call('yay'), call('\n')])


class RendererFailure(RendererTest):
    def setUp(self):
        super(RendererFailure, self).setUp()
        self.renderer.failure('error message')
        self.red_error = colored('error message', 'red')

    def test_prints_message_in_red(self):
        self.stdout.write.assert_has_calls([call(self.red_error), call('\n')])


class RendererSuccess(RendererTest):
    def setUp(self):
        super(RendererSuccess, self).setUp()
        self.renderer.success('sucess message')
        self.green_success = colored('sucess message', 'green')

    def test_prints_message_in_green(self):
        self.stdout.write.assert_has_calls(
            [call(self.green_success), call('\n')])


class RendererAudibleAlert(RendererTest):
    def setUp(self):
        super(RendererAudibleAlert, self).setUp()
        self.renderer.audible_alert(40)

    def test_triggers_the_specified_number_of_bells(self):
        self.stdout.write.assert_called_with('\a' * 40)


class RendererDivider(RendererTest):
    def setUp(self):
        super(RendererDivider, self).setUp()
        self.renderer.divider()

    def test_prints_a_divider_71_characters_wide(self):
        self.stdout.write.assert_has_calls([call('=' * 71), call('\n')])


class RendererReport(RendererTest):
    def setUp(self):
        super(RendererReport, self).setUp()
        self.fake_test = Mock()
        self.fake_test.name = 'FakeTest'
        self.fake_test.changed = 'foo.py'
        self.renderer.report([
            [(self.fake_test, True), (self.fake_test, False)],
            [(self.fake_test, False), (self.fake_test, False)]
        ])

    def test_outputs_color_coded_test_results(self):
        success_name = colored('FakeTest', 'green')
        fail_name = colored('FakeTest', 'red')
        self.stdout.write.assert_has_calls([
            call('Test Report\n'),
            call('\n'),
            call('Test group 1:\t%s, %s' % (success_name, fail_name)),
            call('\n'),
            call('Test group 2:\t%s, %s' % (fail_name, fail_name)),
            call('\n'),
            call('=' * 71),
            call('\n')
        ])


class SingleFilesRendererReport(RendererTest):
    def setUp(self):
        super(SingleFilesRendererReport, self).setUp()
        self.fake_test = Mock()
        self.fake_test.name = 'FakeTest'
        self.fake_test.changed = 'foo.py'
        self.fake_test.all_files = False
        self.renderer.report([
            [(self.fake_test, True), (self.fake_test, False)],
            [(self.fake_test, False), (self.fake_test, False)]
        ])

    def test_outputs_color_coded_test_results_with_short_path(self):
        success_name = colored('FakeTest ()', 'green')
        fail_name = colored('FakeTest ()', 'red')
        self.stdout.write.assert_has_calls([
            call('Test Report\n'),
            call('\n'),
            call('Test group 1:\t%s, %s' % (success_name, fail_name)),
            call('\n'),
            call('Test group 2:\t%s, %s' % (fail_name, fail_name)),
            call('\n'),
            call('=' * 71),
            call('\n')
        ])
