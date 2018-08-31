#!/usr/bin/env python3
from datetime import datetime
from python_lib import metadata, shared, timestore, gitnotes, timelog
from tzlocal import get_localzone
import unittest
import subprocess
import os
import pytz


class Test_metadata(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        shared.set_working_dir(os.getcwd())
        try:
            os.rename(shared.get_gitpath()[:-5] + '.time', shared.get_gitpath()[:-5] + '.time.save')
        except:
            pass

    @classmethod
    def tearDownClass(self):
        try:
            os.rename(shared.get_gitpath()[:-5] + '.time.save', shared.get_gitpath()[:-5] + '.time')
        except:
            pass

    def setUp(self):
        print(" In method", self._testMethodName)

    def tearDown(self):
        try:
            os.remove(shared.get_gitpath()[:-5] + '.time/tempfile')
        except:
            pass

    def test_time_format(self):
        #print('Testing time format')
        format = shared.get_time_format()
        
        local_tz = get_localzone()
        tz = pytz.timezone(str(local_tz))
        now = datetime.utcnow()
        now = tz.localize(now)
        
        expected = now.replace(hour=int(10), minute=int(10))
        self.assertEqual(metadata.time(chour=10, cminute=10), expected.strftime(format))

    def test_meta_data_cleaner_time(self):
        #print('Testing time regex cleaner')
        starts = ['[davidcarl][start]2018-08-28T08:19:45+0200', '[davidcarl][start]2018-08-28T15:00:45+0200']
        self.assertEqual(metadata.get_clean_time_meta_data(starts), ['2018-08-28T08:19:45+0200', '2018-08-28T15:00:45+0200'])

    def test_meta_data_cleaner_name(self):
        #print('Testing name regex cleaner')
        starts = ['[davidcarl][start]08-08-2018/12:34', '[davidcarl][start]08-08-2018/15:00']
        self.assertEqual(metadata.get_clean_name_meta_data(starts), 'davidcarl')

    def test_clean_meta_list_username(self):
        #print('Testing clean meta list username')
        testdata = ['[][end]2018-08-28T15:00:45+0200',
        '[asdasdasdasdasdasdasdasdasdasdasdasdasdasd][start]2018-08-28T15:00:45+0200',
        '[davidcarl][end]2018-08-28T15:00:45+0200']
        result = ['[davidcarl][end]2018-08-28T15:00:45+0200']
        self.assertEqual(metadata.clean_meta_list(testdata), result)

    def test_clean_meta_list_time(self):
        #print('Testing clean meta list time')
        testdata = ['[davidcarl][end]2018-08-28T15:00:45+0200', 
        '[davidcarl][end]2018-08-28T15:60:45+0200', 
        '[davidcarl][start]2018-08-28T24:34:45+0200',
        '[davidcarl][start]2018-08-28T12:34:45+0200']
        result = ['[davidcarl][end]2018-08-28T15:00:45+0200', 
        '[davidcarl][start]2018-08-28T12:34:45+0200']
        self.assertEqual(metadata.clean_meta_list(testdata), result)

    def test_clean_meta_list_tag(self):
        #print('Testing clean meta list tag')
        testdata = ['[davidcarl][end]2018-08-28T15:00:45+0200', 
        '[davidcarl][en]2018-08-28T15:34:45+0200', 
        '[davidcarl][start]2018-08-28T12:34:45+0200',
        '[davidcarl][strt]2018-08-28T12:34:45+0200']
        result = ['[davidcarl][end]2018-08-28T15:00:45+0200', 
        '[davidcarl][start]2018-08-28T12:34:45+0200']
        self.assertEqual(metadata.clean_meta_list(testdata), result)

    def test_clean_meta_list_user_note(self):
        #print('Testing clean meta list user notes')
        testdata = ['Tester det her',
        '[davidcarl][end]2018-08-28T15:00:45+0200']
        result = ['[davidcarl][end]2018-08-28T15:00:45+0200']
        self.assertEqual(metadata.clean_meta_list(testdata), result)

    def test_workcalculator(self):
        #print('Testing time calculator')
        starts = ['[davidcarl][start]2018-08-28T12:34:45+0200', '[davidcarl][start]2018-08-28T15:00:45+0200']
        ended = ['[davidcarl][end]2018-08-28T13:34:45+0200', '[davidcarl][end]2018-08-28T15:30:45+0200']
        self.assertEqual(metadata.calc_time_worked(starts, ended), 5400)

    def test_workcalculator_uneven(self):
        #print('Testing time calculator')
        starts = ['[davidcarl][start]2018-08-28T12:34:45+0200', '[davidcarl][start]2018-08-28T13:40:45+0200', '[davidcarl][start]2018-08-28T16:34:45+0200']
        ended = ['[davidcarl][end]2018-08-28T13:34:45+0200', '[davidcarl][end]2018-08-28T15:30:45+0200']
        self.assertEqual(metadata.calc_time_worked(starts, ended), 10200)

    def test_log_write(self):
        self.assertEqual(timelog.log_type('start'), True)

    def test_log_start_end_logging(self):
        timelog.log_type('start')
        self.assertEqual(timelog.log_type('end'), True)

    def test_log_double_start_logging(self):
        timelog.log_type('start')
        self.assertEqual(timelog.log_type('start'), False)

    def test_log_double_end_logging(self):
        timelog.log_type('end')
        self.assertEqual(timelog.log_type('end'), False)

    def test_log_3rd_party_end_self(self):
        timelog.log_type('start')
        timestore.writetofile(['[bo]][start]2018-08-28T13:40:45+0200'])
        self.assertEqual(timelog.log_type('end'), True)
    
    def test_log_3rd_party_start_self(self):
        timelog.log_type('start')
        timestore.writetofile(['[bo]][start]2018-08-28T13:40:45+0200'])
        self.assertEqual(timelog.log_type('start'), False)

    def test_log_multiple_start_end(self):
        timelog.log_type('start')
        timelog.log_type('end')
        timelog.log_type('start')
        timelog.log_type('end')
        timelog.log_type('start')
        self.assertEqual(timelog.log_type('end'), True)

    def test_log_with_custom_time_t1(self):
        self.assertEqual(timelog.log_type('start', value="1400"), True)

    def test_log_with_custom_time_t2(self):
        self.assertFalse(timelog.log_type('start', value="140"))

    def test_log_with_custom_time_t3(self):
        self.assertEqual(timelog.log_type('start', value="14:00"), True)

    def test_log_with_custom_time_t4(self):
        self.assertEqual(timelog.log_type('start'), True)
    
    def test_check_all_closed_good_data(self):
        data = ['[alfen321][start]2018-08-28T13:14:45+0200','[alfen321][end]2018-08-28T13:14:45+0200',\
                '[alfen321][start]2018-08-28T13:33:45+0200','[alfen321][end]2018-08-28T13:33:45+0200']
        self.assertTrue(metadata.check_all_closed(data))

    def test_check_all_closed_bad_data(self):
        data = ['[alfen321][start]20-08-2018/13:14','[alfen321][end]20-08-2018/13:14',\
                'some random note', 'something else that has nothing to do with timereg',\
                '[alfen321][start]20-08-2018/13:33','[alfen321][end]20-08-2018/13:33']
        self.assertTrue(metadata.check_all_closed(data))

    def test_check_all_closed_missing_end(self):
        data = ['[alfen321][start]2018-08-28T13:14:45+0200','[alfen321][end]2018-08-28T13:14:45+0200',\
                '[alfen321][start]2018-08-28T13:33:45+0200']
        self.assertFalse(metadata.check_all_closed(data))
  
    def test_check_all_closed_missing_start(self):
        data = ['[alfen321][start]2018-08-28T13:14:45+0200','[alfen321][end]2018-08-28T13:14:45+0200',\
                '[alfen321][end]2018-08-28T13:33:45+0200']
        self.assertFalse(metadata.check_all_closed(data))

class Test_shared(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        shared.set_working_dir(os.getcwd())

    def setUp(self):
        print(' In method', self._testMethodName)

    def test_set_different_path_case_root(self):
        shared.set_working_dir('/home/usr/Documents')
        expected = '/home/usr/Documents'
        self.assertEqual(shared.get_work_dir(), expected)

    def test_set_different_path_case_subfolder(self):
        shared.set_working_dir('./home/usr/Documents')
        expected = os.getcwd() + '/home/usr/Documents'
        self.assertEqual(shared.get_work_dir(), expected)

    def test_set_different_path_case_up_two_folders(self):
        shared.set_working_dir('../../home/usr/Documents')
        expected = '/'.join(os.getcwd().split('/')[:-2]) + '/home/usr/Documents'
        self.assertEqual(shared.get_work_dir(), expected)

    def test_git_variables(self):
        result = shared.get_git_variables()
        expected = 'https://www.github.com/prolike/timereg'
        self.assertEqual(result['url'], expected)

    def test_git_path_finding(self):
        expected = os.getcwd() + "/.git/"
        self.assertEqual(shared.get_gitpath(), expected)

class Test_gitmytest(unittest.TestCase):
    
    def setUp(self):
        shared.set_working_dir(os.getcwd())
        print(" In method", self._testMethodName)

    def test_runable(self):
        run = subprocess.run(['python3', 'git-mytest.py', '-h'], stdout=subprocess.PIPE)
        self.assertEqual(run.returncode, 0)

class Test_timestore(unittest.TestCase):

    @classmethod
    def tearDownClass(self):
        shared.set_working_dir(os.getcwd())
        subprocess.call(['rm', '-rf', './test/test_env'], stdout=None, stderr=None)

    def setUp(self):
        shared.set_working_dir(os.getcwd())
        print(' In method', self._testMethodName)

    def test_listsplitter(self):
        testdata = ['[davidcarl][end]08-08-2018/15:39', 
        '[davidcarl][end]08-08-2018/15:00', 
        '[davidcarl][start]08-08-2018/23:34',
        '[davidcarl][start]08-08-2018/15:00']
        start_list, end_list = timestore.listsplitter(testdata)
        self.assertEqual(start_list, ['[davidcarl][start]08-08-2018/23:34', '[davidcarl][start]08-08-2018/15:00'])
        self.assertEqual(end_list, ['[davidcarl][end]08-08-2018/15:39', '[davidcarl][end]08-08-2018/15:00'])

    def test_dump_no_data(self):
        subprocess.call(['bash', './test/scripts/Setup'], stdout=None, stderr=None)        
        shared.set_working_dir('./test/test_env/clone1')
        timestore.dump()

    def test_dump_good_data(self):
        subprocess.call(['bash', './test/scripts/Setup'], stdout=None, stderr=None)
        subprocess.call(['bash', './test/scripts/timestore_data_good_data'], stdout=None, stderr=None)
        shared.set_working_dir('./test/test_env/clone1')
        timestore.dump()
        notes = gitnotes.get_all_notes()
        for key, value in notes.items():
            self.assertEqual(len(value), 4)
        self.assertFalse(os.path.isfile('./test/test_env/clone1/.time/tempfile'))


    def test_dump_bad_data(self):
        subprocess.call(['bash', './test/scripts/Setup'], stdout=None, stderr=None)
        subprocess.call(['bash', './test/scripts/timestore_data_bad_data'], stdout=None, stderr=None)
        shared.set_working_dir('./test/test_env/clone1')
        timestore.dump()
        notes = gitnotes.get_all_notes()
        self.assertFalse(notes)
        self.assertTrue(os.path.isfile('./test/test_env/clone1/.time/tempfile'))
        
    
class Test_gitnotes(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        shared.set_quiet_mode(True)

    @classmethod
    def tearDownClass(self):
        shared.set_working_dir(os.getcwd())
        subprocess.call(['rm', '-rf', './test/test_env'], stdout=None, stderr=None)    

    def setUp(self):
        print(" In method", self._testMethodName)

    def test_get_all_notes(self):
        subprocess.call(['bash', './test/scripts/Setup'], stdout=None, stderr=None)
        subprocess.call(['bash', './test/scripts/test_get_all_notes'], stdout=None, stderr=None)

        shared.set_working_dir('./test/test_env/origin')
        result = gitnotes.get_all_notes()
        commits = subprocess.run(['bash', './test/scripts/get_commits'], stdout=subprocess.PIPE).stdout.decode('utf-8').rstrip().split(' ')
        expected = {commits[0]: ['note1', 'note2', 'note3', 'note4', 'note5', 'note6', 'note7'], 
                    commits[1]: ['1note', '2note', '3note', '4note', '5note', '6note', '7note']}

        self.assertEqual(result, expected)

    def test_git_fetch_notes_no_conflict_no_notes_history(self):
        subprocess.call(['bash', './test/scripts/Setup'], stdout=None, stderr=None)
        subprocess.call(['bash', './test/scripts/test_fetch_no_conflict_no_notes_history'], stdout=None, stderr=None)
        
        shared.set_working_dir('./test/test_env/clone1')
        gitnotes.fetch_notes()

        with open('./test/test_env/origin/.git/refs/notes/commits', 'r') as f:
            origin = f.read()        
        with open('./test/test_env/clone1/.git/refs/notes/commits', 'r') as f:
            clone = f.read()        
        self.assertEqual(origin, clone)
    
    def test_git_push_notes_no_conflict(self):
        subprocess.call(['bash', './test/scripts/test_push_no_conflict_no_notes_history'])

        shared.set_working_dir('./test/test_env/clone1')
        gitnotes.push_notes()

        with open('./test/test_env/origin/.git/refs/notes/commits', 'r') as f:
            origin = f.read()        
        with open('./test/test_env/clone1/.git/refs/notes/commits', 'r') as f:
            clone = f.read()        
        self.assertEqual(origin, clone)

    def test_git_fetch_merge_conflict_different_commits_no_notes_history(self):
        subprocess.call(['bash', './test/scripts/Setup'], stdout=None, stderr=None)    
        subprocess.call(['bash', './test/scripts/test_fetch_merge_conflict_different_commits_no_notes_history'],\
                            stdout=None, stderr=None)
        shared.set_working_dir('./test/test_env/clone1')
        gitnotes.fetch_notes()
        
        call = ['git', '-C', './teset/test_env/origin', 'notes', 'list']
        origin = subprocess.run(call, stdout=subprocess.PIPE).stdout.decode('utf-8').split('\n')
        call[2] = './teset/test_env/clone1'
        clone = subprocess.run(call, stdout=subprocess.PIPE).stdout.decode('utf-8').split('\n')

        for line in origin:
            if line not in clone:
                self.fail("missing notes from origin")
        
    def test_git_fetch_merge_conflict_same_commits_no_notes_history(self):
        subprocess.call(['bash', './test/scripts/Setup'], stdout=None, stderr=None)    
        subprocess.call(['bash', './test/scripts/test_fetch_merge_conflict_same_commit_no_notes_history'], \
                            stdout=None, stderr=None)
        shared.set_working_dir('./test/test_env/clone1')
        gitnotes.fetch_notes()

        clone = gitnotes.get_all_notes()
        shared.set_working_dir('./test/test_env/origin')
        origin = gitnotes.get_all_notes()
        
        for key, notelist in origin.items():
            clone_list = clone[key]
            for note in notelist:
                if note not in clone_list:
                    self.fail("missing notes from origin")


    def test_git_push_merge_conflict_same_commit_with_notes_history(self):
        subprocess.call(['bash', './test/scripts/Setup'], stdout=None, stderr=None)    
        subprocess.call(['bash', './test/scripts/test_push_merge_conflict_same_commit_with_notes_history'], \
                            stdout=None, stderr=None)
        shared.set_working_dir('./test/test_env/clone1')
        gitnotes.push_notes()

        clone = gitnotes.get_all_notes()
        shared.set_working_dir('./test/test_env/origin')
        origin = gitnotes.get_all_notes()
        
        for key, notelist in origin.items():
            clone_list = clone[key]
            for note in notelist:
                if note not in clone_list:
                    self.fail("missing notes from origin")


if __name__ == '__main__':
    unittest.main()