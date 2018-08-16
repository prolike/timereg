#!/usr/bin/env python3
from datetime import datetime
from python_lib import metadata, shared, timestore
import unittest
import subprocess
import os


class Test_metadata(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        try:
            os.rename(shared.get_gitpath()[:-5] + '.time/tempfile', shared.get_gitpath()[:-5] + '.time/tempfile.save')
            subprocess.run(['ls', '.time'])
        except:
            pass

    @classmethod
    def tearDownClass(self):
        try:
            os.rename(shared.get_gitpath()[:-5] + '.time/tempfile.save', shared.get_gitpath()[:-5] + '.time/tempfile')
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


class Test_shared(unittest.TestCase):

    def setUp(self):
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
        print(" In method", self._testMethodName)

    def test_runable(self):
        run = subprocess.run(['python3', 'git-mytest.py', '-h'], stdout=subprocess.PIPE)
        self.assertEqual(run.returncode, 0)

class Test_timestore(unittest.TestCase):

    def setUp(self):
        print(' In method', self._testMethodName)

if __name__ == '__main__':
    unittest.main()