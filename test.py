#!/usr/bin/env python3
from datetime import datetime
from python_lib import metadata, shared, timestore, gitnotes
import unittest
import subprocess
import os


class Test_metadata(unittest.TestCase):

    @classmethod
    def setUpClass(self):
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
        shared.set_working_dir(os.getcwd())
        print(" In method", self._testMethodName)

    def tearDown(self):
        try:
            os.remove(shared.get_gitpath()[:-5] + '.time/tempfile')
        except:
            pass

    def test_time_format(self):
        #print('Testing time format')
        format = '%d-%m-%Y/%H:%M'
        expected = datetime.now().replace(hour=int(10), minute=int(10))
        self.assertEqual(metadata.time(chour=10, cminute=10), expected.strftime(format))

    def test_meta_data_cleaner_time(self):
        #print('Testing time regex cleaner')
        starts = ['[davidcarl][start]08-08-2018/12:34', '[davidcarl][start]08-08-2018/15:00']
        self.assertEqual(metadata.get_clean_time_meta_data(starts), ['08-08-2018/12:34', '08-08-2018/15:00'])

    def test_meta_data_cleaner_name(self):
        #print('Testing name regex cleaner')
        starts = ['[davidcarl][start]08-08-2018/12:34', '[davidcarl][start]08-08-2018/15:00']
        self.assertEqual(metadata.get_clean_name_meta_data(starts), 'davidcarl')

    def test_clean_meta_list_username(self):
        #print('Testing clean meta list username')
        testdata = ['[][end]08-08-2018/12:34',
        '[asdasdasdasdasdasdasdasdasdasdasdasdasdasd][start]08-08-2018/12:34',
        '[davidcarl][end]08-08-2018/12:34']
        result = ['[davidcarl][end]08-08-2018/12:34']
        self.assertEqual(metadata.clean_meta_list(testdata), result)

    def test_clean_meta_list_time(self):
        #print('Testing clean meta list time')
        testdata = ['[davidcarl][end]08-08-2018/15:69', 
        '[davidcarl][end]08-08-2018/15:00', 
        '[davidcarl][start]08-08-2018/25:34',
        '[davidcarl][start]08-08-2018/15:00']
        result = ['[davidcarl][end]08-08-2018/15:00', 
        '[davidcarl][start]08-08-2018/15:00']
        self.assertEqual(metadata.clean_meta_list(testdata), result)

    def test_clean_meta_list_tag(self):
        #print('Testing clean meta list tag')
        testdata = ['[davidcarl][end]08-08-2018/15:00', 
        '[davidcarl][en]08-08-2018/15:00', 
        '[davidcarl][start]08-08-2018/12:34',
        '[davidcarl][strt]08-08-2018/15:00']
        result = ['[davidcarl][end]08-08-2018/15:00', 
        '[davidcarl][start]08-08-2018/12:34']
        self.assertEqual(metadata.clean_meta_list(testdata), result)

    def test_clean_meta_list_user_note(self):
        #print('Testing clean meta list user notes')
        testdata = ['Tester det her',
        '[davidcarl][end]08-08-2018/15:00']
        result = ['[davidcarl][end]08-08-2018/15:00']
        self.assertEqual(metadata.clean_meta_list(testdata), result)

    def test_workcalculator(self):
        #print('Testing time calculator')
        starts = ['[davidcarl][start]08-08-2018/12:34', '[davidcarl][start]08-08-2018/15:00']
        ended = ['[davidcarl][end]08-08-2018/13:34', '[davidcarl][end]08-08-2018/15:30']
        self.assertEqual(metadata.calc_time_worked(starts, ended), 90)

    def test_workcalculator_uneven(self):
        #print('Testing time calculator')
        starts = ['[davidcarl][start]08-08-2018/12:34', '[davidcarl][start]08-08-2018/13:40', '[davidcarl][start]08-08-2018/15:00']
        ended = ['[davidcarl][end]08-08-2018/13:34', '[davidcarl][end]08-08-2018/15:30']
        self.assertEqual(metadata.calc_time_worked(starts, ended), 170)

    def test_log_write(self):
        self.assertEqual(metadata.log('start'), True)

    def test_log_start_end_logging(self):
        metadata.log('start')
        self.assertEqual(metadata.log('end'), True)

    def test_log_double_start_logging(self):
        metadata.log('start')
        self.assertEqual(metadata.log('start'), False)

    def test_log_double_end_logging(self):
        metadata.log('end')
        self.assertEqual(metadata.log('end'), False)

    def test_log_3rd_party_end_self(self):
        metadata.log('start')
        timestore.writetofile(['[bo]][start]08-08-2018/12:34'])
        self.assertEqual(metadata.log('end'), True)
    
    def test_log_3rd_party_start_self(self):
        metadata.log('start')
        timestore.writetofile(['[bo]][start]08-08-2018/12:34'])
        self.assertEqual(metadata.log('start'), False)

    def test_log_multiple_start_end(self):
        metadata.log('start')
        metadata.log('end')
        metadata.log('start')
        metadata.log('end')
        metadata.log('start')
        self.assertEqual(metadata.log('end'), True)

    def test_log_with_custom_time_t1(self):
        self.assertEqual(metadata.log('start', value="1400"), True)

    def test_log_with_custom_time_t2(self):
        self.assertEqual(metadata.log('start', value="140"), True)

    def test_log_with_custom_time_t3(self):
        self.assertEqual(metadata.log('start', value="14:00"), True)

    def test_log_with_custom_time_t4(self):
        self.assertEqual(metadata.log('start'), True)

class Test_shared(unittest.TestCase):

    def setUp(self):
        shared.set_working_dir(os.getcwd())
        print(" In method", self._testMethodName)

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
        expected = 'git@github.com:prolike/timereg.git'
        self.assertEqual(result['url'], expected)

    def test_git_path_finding(self):
        #print('Testing git path finding')
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