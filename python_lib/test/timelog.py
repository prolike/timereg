import unittest, subprocess, os, time
from python_lib import shared, timelog, git_timestore_calls as gtc, git_timestore, git_objects
# from python_lib.git_objects import *


class Test_timelog(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        shared.set_working_dir(os.getcwd())
        shared.set_quiet_mode(True)
        try:
            os.rename(shared.get_gitpath()[
                      :-5] + '.time', shared.get_gitpath()[:-5] + '.time.save')
        except:
            pass

    @classmethod
    def tearDownClass(self):
        shared.set_working_dir(os.getcwd())
        subprocess.call(['rm', '-rf', './test/test_env'],
                        stdout=None, stderr=None)
        try:
            os.rename(shared.get_gitpath()[
                      :-5] + '.time.save', shared.get_gitpath()[:-5] + '.time')
        except:
            pass

    def setUp(self):
        print(" In method", self._testMethodName)

    def tearDown(self):
        try:
            os.remove(shared.get_gitpath()[:-5] + '.time/tempfile')
        except:
            pass


    def test_log_start_end_logging(self):
        subprocess.call(['bash', './test/scripts/Setup'], stdout=None, stderr=None)
        shared.set_working_dir('./test/test_env/clone2')
        shared.set_issue_number(1)
        self.assertTrue(timelog.log_type('start'))
        self.assertTrue(timelog.log_type('end'))


    def test_log_double_start_logging(self):
        subprocess.call(['bash', './test/scripts/Setup'], stdout=None, stderr=None)
        shared.set_working_dir('./test/test_env/clone2')
        shared.set_issue_number(1)
        timelog.log_type('start')
        self.assertEqual(timelog.log_type('start'), False)


    def test_log_double_end_logging(self):
        subprocess.call(['bash', './test/scripts/Setup'], stdout=None, stderr=None)
        shared.set_working_dir('./test/test_env/clone2')
        shared.set_issue_number(1)
        timelog.log_type('end')
        self.assertEqual(timelog.log_type('end'), False)


    def test_log_3rd_party_end_self(self):
        subprocess.call(['bash', './test/scripts/Setup'], stdout=None, stderr=None)
        shared.set_working_dir('./test/test_env/clone2')
        shared.set_issue_number(1)
        timelog.log_type('start')
        gtc.store(entry={'user':'bo', 'state':'start', 'timestamp':'2018-08-28T13:40:00+0200'}, issue=1)
        self.assertEqual(timelog.log_type('end'), True)


    def test_log_3rd_party_start_self(self):
        subprocess.call(['bash', './test/scripts/Setup'], stdout=None, stderr=None)
        shared.set_working_dir('./test/test_env/clone2')
        shared.set_issue_number(1)
        timelog.log_type('start')
        gtc.store(entry={'user':'bo', 'state':'start', 'timestamp':'2018-08-28T13:40:00+0200'}, issue=1)
        self.assertEqual(timelog.log_type('start'), False)

    # def test_log_multiple_start_end(self):
    #     subprocess.call(['bash', './test/scripts/Setup'], stdout=None, stderr=None)
    #     shared.set_working_dir('./test/test_env/clone2')
    #     shared.set_issue_number(1)
    #     timelog.log_type('start')
    #     time.sleep(0.5)
    #     timelog.log_type('end')
    #     time.sleep(0.5)
    #     timelog.log_type('start')
    #     time.sleep(0.5)
    #     self.assertEqual(timelog.log_type('end'), True)

    def test_log_with_custom_time_t1(self):
        subprocess.call(['bash', './test/scripts/Setup'], stdout=None, stderr=None)
        shared.set_working_dir('./test/test_env/clone2')
        shared.set_issue_number(1)
        sha1 = git_timestore.save_git_blob(git_objects.Blob(
            os.getcwd()+'/test/test_env/origin/issue/1'))
        self.assertTrue(timelog.log_type('start', value='14:00'))
        self.assertEqual(len(gtc.get_all_as_dict()[sha1].keys()), 1)
        self.assertTrue(timelog.log_type('end', value='1405'))
        self.assertEqual(len(gtc.get_all_as_dict()[sha1].keys()), 2)
        self.assertFalse(timelog.log_type('start', value='145'))
        self.assertEqual(len(gtc.get_all_as_dict()[sha1].keys()), 2)
        self.assertTrue(timelog.log_type('start', value='1405'))
        self.assertTrue(timelog.log_type('end', value='1410'))
        self.assertEqual(len(gtc.get_all_as_dict()[sha1].keys()), 4)

    def test_log_with_custom_time_t2(self):
        subprocess.call(['bash', './test/scripts/Setup'], stdout=None, stderr=None)
        shared.set_working_dir('./test/test_env/clone2')
        shared.set_issue_number(1)
        sha1 = git_timestore.save_git_blob(git_objects.Blob(
            os.getcwd()+'/test/test_env/origin/issue/1'))
        self.assertFalse(timelog.log_type('did', value=''))
        self.assertTrue(sha1 not in gtc.get_all_as_dict())
        self.assertTrue(timelog.log_type('did', value='2h'))
        self.assertEqual(len(gtc.get_all_as_dict()[sha1].keys()), 2)
        shared.set_working_dir('./test/test_env/clone1')
        self.assertTrue(sha1 not in gtc.get_all_as_dict())
        self.assertTrue(timelog.log_type('did', value='12h'))
        self.assertEqual(len(gtc.get_all_as_dict()[sha1].keys()), 2)
        self.assertTrue(timelog.log_type('start'))
        self.assertTrue(timelog.log_type('end'))


if __name__ == '__main__':
    unittest.main()