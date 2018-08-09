#!/usr/bin/env python3
from datetime import datetime
from python_lib import main as mainfile
import unittest


class TestAdd(unittest.TestCase):

    def test_time_format(self):
        print('Testing time format')
        format = '%d-%m-%Y/%H:%M'
        expected = datetime.now().replace(hour=int(10), minute=int(10))
        self.assertEqual(mainfile.time(chour=10, cminute=10), expected.strftime(format))

    def test_meta_data_cleaner_time(self):
        print('Testing time regex cleaner')
        starts = ['[davidcarl][start]08-08-2018/12:34', '[davidcarl][start]08-08-2018/15:00']
        self.assertEqual(mainfile.get_clean_time_meta_data(starts), ['08-08-2018/12:34', '08-08-2018/15:00'])

    def test_meta_data_cleaner_name(self):
        print('Testing name regex cleaner')
        starts = ['[davidcarl][start]08-08-2018/12:34', '[davidcarl][start]08-08-2018/15:00']
        self.assertEqual(mainfile.get_clean_name_meta_data(starts), 'davidcarl')

    def test_clean_meta_list_username(self):
        print('Testing clean meta list username')
        testdata = ['[][end]08-08-2018/12:34',
        '[asdasdasdasdasdasdasdasdasdasdasdasdasdasd][start]08-08-2018/12:34',
        '[davidcarl][end]08-08-2018/12:34']
        result = ['[davidcarl][end]08-08-2018/12:34']
        self.assertEqual(mainfile.clean_meta_list(testdata), result)

    def test_clean_meta_list_time(self):
        print('Testing clean meta list time')
        testdata = ['[davidcarl][end]08-08-2018/15:69', 
        '[davidcarl][end]08-08-2018/15:00', 
        '[davidcarl][start]08-08-2018/25:34',
        '[davidcarl][start]08-08-2018/15:00']
        result = ['[davidcarl][end]08-08-2018/15:00', 
        '[davidcarl][start]08-08-2018/15:00']
        self.assertEqual(mainfile.clean_meta_list(testdata), result)

    def test_clean_meta_list_tag(self):
        print('Testing clean meta list tag')
        testdata = ['[davidcarl][end]08-08-2018/15:00', 
        '[davidcarl][en]08-08-2018/15:00', 
        '[davidcarl][start]08-08-2018/12:34',
        '[davidcarl][strt]08-08-2018/15:00']
        result = ['[davidcarl][end]08-08-2018/15:00', 
        '[davidcarl][start]08-08-2018/12:34']
        self.assertEqual(mainfile.clean_meta_list(testdata), result)

    def test_clean_meta_list_user_note(self):
        print('Testing clean meta list user notes')
        testdata = ['Tester det her',
        '[davidcarl][end]08-08-2018/15:00']
        result = ['[davidcarl][end]08-08-2018/15:00']
        self.assertEqual(mainfile.clean_meta_list(testdata), result)

    def test_workcalculator(self):
        print('Testing time calculator')
        starts = ['[davidcarl][start]08-08-2018/12:34', '[davidcarl][start]08-08-2018/15:00']
        ended = ['[davidcarl][end]08-08-2018/13:34', '[davidcarl][end]08-08-2018/15:30']
        self.assertEqual(mainfile.calc_time_worked(starts, ended), 90)

if __name__ == '__main__':
    unittest.main()