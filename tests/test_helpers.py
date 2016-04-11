from . import Mock, patch, unittest

from testtube.helpers import (
    Frosted, HardTestFailure, Nosetests, Pep8, PythonSetupPyTest)


class HelperTests(unittest.TestCase):
    helper_conf = {}
    helper_class = Pep8
    subprocess_result = 0
    src_dir = '/fake/path'
    test_path = 'fake_path.py'
    execute_test = True

    def setUp(self):
        subproc_patcher = patch('testtube.helpers.subprocess')
        self.addCleanup(subproc_patcher.stop)
        self.subprocess = subproc_patcher.start()
        self.subprocess.call.return_value = self.subprocess_result

        settings_patcher = patch('testtube.helpers.Settings')
        self.addCleanup(settings_patcher.stop)
        self.settings = settings_patcher.start()
        self.settings.SRC_DIR = self.src_dir

        self.renderer = Mock()

        self.helper = self.helper_class(**self.helper_conf)
        self.helper.renderer = self.renderer
        self.fake_match_obj = Mock()

        self.result = None

        if self.execute_test:
            self.result = self.helper('fake_path.py', self.fake_match_obj)


class Pep8Helper(HelperTests):
    def test_invokes_the_pep8_command_against_a_specified_path(self):
        self.subprocess.call.assert_called_once_with(['pep8', 'fake_path.py'])

    def test_outputs_testing_notice(self):
        self.renderer.notice.assert_any_call(
            'Executing Pep8 against fake_path.py.\n')

    def test_outputs_success_message_if_tests_pass(self):
        self.renderer.success.assert_called_once_with('Test passed.')

    def test_returns_true_if_tests_pass(self):
        self.assertTrue(self.result)


class Pep8HelperOnTestFailure(HelperTests):
    subprocess_result = 1

    def test_audibly_rings(self):
        self.renderer.audible_alert.assert_called_once_with(3)

    def test_outputs_failure_notice(self):
        self.renderer.failure.assert_called_once_with('Test failed.')


class Pep8HelperOnTestFailureWithFailFastEnabled(HelperTests):
    helper_conf = {'fail_fast': True}
    subprocess_result = 1
    execute_test = False

    def test_raises_HardTestFailure(self):
        self.assertRaises(
            HardTestFailure, self.helper, 'fake_path.py', self.fake_match_obj)


class Pep8HelperWithInvalidTestCommand(HelperTests):
    helper_conf = {'command': None}

    def test_doesnt_invoke_a_subprocess(self):
        self.assertFalse(self.subprocess.call.called)

    def test_passes(self):
        self.assertTrue(self.result)


class Pep8HelperConfiguredToCheckEntireSrcDir(HelperTests):
    helper_conf = {'all_files': True}

    def test_runs_pep8_againts_entire_src_dir(self):
        self.subprocess.call.assert_called_once_with(['pep8', '/fake/path'])

    def test_outputs_test_notice_without_specific_path(self):
        self.renderer.notice.assert_any_call(
            'Executing Pep8 against source directory.\n')


class FrostedHelperConfiguredToCheckAllFiles(HelperTests):
    helper_class = Frosted
    helper_conf = {'all_files': True}

    def test_adds_r_flag_when_passing_settings_dir_to_frosted_cmd(self):
        """adds -r flag when passing settings dir to frosted"""
        self.subprocess.call.assert_called_once_with(
            ['frosted', '-r', '/fake/path'])


class FrotedHelperNotConfiguredToCheckAllFiles(HelperTests):
    helper_class = Frosted

    def test_only_checks_the_changed_file_and_doesnt_use_any_flags(self):
        self.subprocess.call.assert_called_once_with(
            ['frosted', 'fake_path.py'])


class NosetestsHelper(HelperTests):
    helper_conf = {'all_files': False, 'name': 'tests'}
    helper_class = Nosetests

    def test_doesnt_allow_itself_to_be_configured_to_check_single_files(self):
        self.assertTrue(self.helper.all_files)

    def test_does_allow_itself_to_be_configured_with_other_options(self):
        self.assertEqual(self.helper.name, 'tests')


class PythonSetupPyHelper(HelperTests):
    """PythonSetupPy helper"""
    helper_class = PythonSetupPyTest

    def test_always_uses_setup_py_test_as_args(self):
        """always uses 'setup.py test' as args"""
        self.subprocess.call.assert_called_once_with(
            ['python', 'setup.py', 'test'])
