#!/usr/bin/env python3
from datetime import datetime
import main as mainfile
import unittest


class TestAdd(unittest.TestCase):

    def test_timeformat(self):
        format = "%d-%m-%Y/%H:%M"
        expected = datetime.now().replace(hour=int(10), minute=int(10))
        self.assertEqual(mainfile.time(chour=10, cminute=10), expected.strftime(format))

    def test_metadatacleanertime(self):
        starts = ['[davidcarl][start]08-08-2018/12:34', '[davidcarl][start]08-08-2018/15:00']
        self.assertEqual(mainfile.get_clean_time_meta_data(starts), ['08-08-2018/12:34', '08-08-2018/15:00'])

    def test_metadatacleanername(self):
        starts = ['[davidcarl][start]08-08-2018/12:34', '[davidcarl][start]08-08-2018/15:00']
        self.assertEqual(mainfile.get_clean_name_meta_data(starts), 'davidcarl')

    def test_cleanmetalist(self):
        testdata = ['[][end]08-08-2018/12:34', 
        '[davidcarl][end]08-08-2018/15:69', 
        '[davidcarl][end]08-08-2018/15:00', 
        '[asdasdasdasdasdasdasdasdasdasdasdasdasdasd][start]08-08-2018/12:34', 
        '[davidcarl][star]08-08-2018/15:00', 
        '[davidcarl][start]08-08-2018/12:34',
        '[davidcarl][strt]08-08-2018/15:00']
        result = ['[davidcarl][end]08-08-2018/15:00', 
        '[davidcarl][start]08-08-2018/12:34']
        self.assertEqual(mainfile.clean_meta_list(testdata), result)

    #def test_metadatacleanername_wrong(self):


    #def test_metadatacleanertime_wrong(self):


    def test_workcalculator(self):
        starts = ['[davidcarl][start]08-08-2018/12:34', '[davidcarl][start]08-08-2018/15:00']
        ended = ['[davidcarl][end]08-08-2018/13:34', '[davidcarl][end]08-08-2018/15:30']
        self.assertEqual(mainfile.calc_time_worked(starts, ended), 90)

if __name__ == '__main__':
    unittest.main()