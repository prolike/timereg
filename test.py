#!/usr/bin/env python3
from datetime import datetime
from python_lib import metadata, shared, timestore, timelog
from python_lib import git_timestore_calls as gtc, git_objects, git_timestore
from tzlocal import get_localzone
from collections import defaultdict
import logging
import unittest
import subprocess
import os, sys
import pytz
import importlib


# uncommenent to enable verbose :)  
# importlib.reload(logging)
# logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)

# class Test_timelog(unittest.TestCase):

#     @classmethod
#     def setUpClass(self):
#         shared.set_working_dir(os.getcwd())
#         shared.set_quiet_mode(True)
#         try:
#             os.rename(shared.get_gitpath()[:-5] + '.time', shared.get_gitpath()[:-5] + '.time.save')
#         except:
#             pass

#     @classmethod
#     def tearDownClass(self):
#         shared.set_working_dir(os.getcwd())
#         subprocess.call(['rm', '-rf', './test/test_env'], stdout=None, stderr=None)  
#         try:
#             os.rename(shared.get_gitpath()[:-5] + '.time.save', shared.get_gitpath()[:-5] + '.time')
#         except:
#             pass

#     def setUp(self):
#         print(" In method", self._testMethodName)

#     def tearDown(self):
#         try:
#             os.remove(shared.get_gitpath()[:-5] + '.time/tempfile')
#         except:
#             pass

#     def test_log_start_end_logging(self):
#         subprocess.call(['bash', './test/scripts/Setup'], stdout=None, stderr=None)        
#         shared.set_working_dir('./test/test_env/clone2')
#         shared.set_issue_number(1)
#         self.assertTrue(timelog.log_type('start'))
#         self.assertTrue(timelog.log_type('end'))

#     def test_log_double_start_logging(self):
#         subprocess.call(['bash', './test/scripts/Setup'], stdout=None, stderr=None)        
#         shared.set_working_dir('./test/test_env/clone2')
#         shared.set_issue_number(1)
#         timelog.log_type('start')
#         self.assertEqual(timelog.log_type('start'), False)

#     def test_log_double_end_logging(self):
#         subprocess.call(['bash', './test/scripts/Setup'], stdout=None, stderr=None)        
#         shared.set_working_dir('./test/test_env/clone2')
#         shared.set_issue_number(1)
#         timelog.log_type('end')
#         self.assertEqual(timelog.log_type('end'), False)

#     def test_log_3rd_party_end_self(self):
#         subprocess.call(['bash', './test/scripts/Setup'], stdout=None, stderr=None)        
#         shared.set_working_dir('./test/test_env/clone2')
#         shared.set_issue_number(1)
#         timelog.log_type('start')
#         timestore.writetofile(['[bo]][start]2018-08-28T13:40:45+0200'])
#         self.assertEqual(timelog.log_type('end'), True)
    
#     def test_log_3rd_party_start_self(self):
#         subprocess.call(['bash', './test/scripts/Setup'], stdout=None, stderr=None)        
#         shared.set_working_dir('./test/test_env/clone2')
#         shared.set_issue_number(1)
#         timelog.log_type('start')
#         timestore.writetofile(['[bo]][start]2018-08-28T13:40:45+0200'])
#         self.assertEqual(timelog.log_type('start'), False)

#     def test_log_multiple_start_end(self):
#         subprocess.call(['bash', './test/scripts/Setup'], stdout=None, stderr=None)        
#         shared.set_working_dir('./test/test_env/clone2')
#         shared.set_issue_number(1)
#         timelog.log_type('start')
#         timelog.log_type('end')
#         timelog.log_type('start')
#         timelog.log_type('end')
#         timelog.log_type('start')
#         self.assertEqual(timelog.log_type('end'), True)

#     def test_log_with_custom_time_t1(self):
#         subprocess.call(['bash', './test/scripts/Setup'], stdout=None, stderr=None)        
#         shared.set_working_dir('./test/test_env/clone2')
#         shared.set_issue_number(1)
#         self.assertTrue(timelog.log_type('start', value='14:00'))
#         self.assertEqual(len(gtc.get_all_as_list()), 1)
#         self.assertTrue(timelog.log_type('end', value='1405'))
#         self.assertEqual(len(gtc.get_all_as_list()), 2)
#         self.assertFalse(timelog.log_type('start', value='145'))
#         self.assertEqual(len(gtc.get_all_as_list()), 2)
#         self.assertTrue(timelog.log_type('start', value='1405'))
#         self.assertTrue(timelog.log_type('end', value='1410'))
#         self.assertEqual(len(gtc.get_all_as_list()), 4)

#     def test_log_with_custom_time_t2(self):
#         subprocess.call(['bash', './test/scripts/Setup'], stdout=None, stderr=None)        
#         shared.set_working_dir('./test/test_env/clone2')
#         shared.set_issue_number(1)
#         self.assertFalse(timelog.log_type('did', value = ''))
#         self.assertEqual(len(gtc.get_all_as_list()), 0)
#         self.assertTrue(timelog.log_type('did', value = '2h'))
#         self.assertEqual(len(gtc.get_all_as_list()), 2)
#         shared.set_working_dir('./test/test_env/clone1')
#         self.assertEqual(len(gtc.get_all_as_list()), 0)
#         self.assertTrue(timelog.log_type('did', value = '12h'))
#         self.assertEqual(len(gtc.get_all_as_list()), 2)
#         self.assertTrue(timelog.log_type('start'))
#         self.assertTrue(timelog.log_type('end'))

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
        format = shared.get_time_format()
        
        local_tz = get_localzone()
        tz = pytz.timezone(str(local_tz))
        now = datetime.utcnow()
        now = tz.localize(now)
        
        expected = now.replace(hour=int(10), minute=int(10))
        self.assertEqual(metadata.time(chour=10, cminute=10), expected.strftime(format))

    def test_meta_data_cleaner_time(self):
        starts = ['[davidcarl][start]2018-08-28T08:19:45+0200', '[davidcarl][start]2018-08-28T15:00:45+0200']
        self.assertEqual(metadata.get_clean_time_meta_data(starts), ['2018-08-28T08:19:45+0200', '2018-08-28T15:00:45+0200'])

    def test_meta_data_cleaner_name(self):
        starts = ['[davidcarl][start]08-08-2018/12:34', '[davidcarl][start]08-08-2018/15:00']
        self.assertEqual(metadata.get_clean_name_meta_data(starts), 'davidcarl')

    def test_clean_meta_list_username(self):
        testdata = ['[][end]2018-08-28T15:00:45+0200',
        '[asdasdasdasdasdasdasdasdasdasdasdasdasdasd][start]2018-08-28T15:00:45+0200',
        '[davidcarl][end]2018-08-28T15:00:45+0200']
        result = ['[davidcarl][end]2018-08-28T15:00:45+0200']
        self.assertEqual(metadata.clean_meta_list(testdata), result)

    def test_clean_meta_list_time(self):
        testdata = ['[davidcarl][end]2018-08-28T15:00:45+0200', 
        '[davidcarl][end]2018-08-28T15:60:45+0200', 
        '[davidcarl][start]2018-08-28T24:34:45+0200',
        '[davidcarl][start]2018-08-28T12:34:45+0200']
        result = ['[davidcarl][end]2018-08-28T15:00:45+0200', 
        '[davidcarl][start]2018-08-28T12:34:45+0200']
        self.assertEqual(metadata.clean_meta_list(testdata), result)

    def test_clean_meta_list_tag(self):
        testdata = ['[davidcarl][end]2018-08-28T15:00:45+0200', 
        '[davidcarl][en]2018-08-28T15:34:45+0200', 
        '[davidcarl][start]2018-08-28T12:34:45+0200',
        '[davidcarl][strt]2018-08-28T12:34:45+0200']
        result = ['[davidcarl][end]2018-08-28T15:00:45+0200', 
        '[davidcarl][start]2018-08-28T12:34:45+0200']
        self.assertEqual(metadata.clean_meta_list(testdata), result)

    def test_clean_meta_list_user_note(self):
        testdata = ['Tester det her',
        '[davidcarl][end]2018-08-28T15:00:45+0200']
        result = ['[davidcarl][end]2018-08-28T15:00:45+0200']
        self.assertEqual(metadata.clean_meta_list(testdata), result)

    def test_workcalculator(self):
        starts = ['[davidcarl][start]2018-08-28T12:34:45+0200', '[davidcarl][start]2018-08-28T15:00:45+0200']
        ended = ['[davidcarl][end]2018-08-28T13:34:45+0200', '[davidcarl][end]2018-08-28T15:30:45+0200']
        self.assertEqual(metadata.calc_time_worked(starts, ended), 5400)

    def test_workcalculator_uneven(self):
        starts = ['[davidcarl][start]2018-08-28T12:34:45+0200', '[davidcarl][start]2018-08-28T13:40:45+0200', '[davidcarl][start]2018-08-28T16:34:45+0200']
        ended = ['[davidcarl][end]2018-08-28T13:34:45+0200', '[davidcarl][end]2018-08-28T15:30:45+0200']
        self.assertEqual(metadata.calc_time_worked(starts, ended), 10200)
    
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

    def test_get_date_string(self):
        self.assertEqual(metadata.get_date('[alfen321][start]2018-08-28T13:14:45+0200'), '2018-08-28')
    
    def test_get_date_list(self):
        data = ['[alfen321][start]2018-08-28T13:14:45+0200','[alfen321][end]2018-08-28T13:14:45+0200']
        res = ['2018-08-28', '2018-08-28']
        self.assertEqual(metadata.get_date(data), res)

    def test_order_days(self):
        data = ['[davidcarl][start]2018-09-04T09:00:00+0200',
                '[davidcarl][end]2018-09-04T09:10:00+0200',
                'davidcarl][start]2018-09-01T09:00:00+0200',
                '[davidcarl][end]2018-09-01T09:10:00+0200']
        res = ['davidcarl][start]2018-09-01T09:00:00+0200',
                '[davidcarl][end]2018-09-01T09:10:00+0200',
                '[davidcarl][start]2018-09-04T09:00:00+0200',
                '[davidcarl][end]2018-09-04T09:10:00+0200']
        self.assertEqual(metadata.order_days(data), res)
    
    def test_extract_time_string(self):
        self.assertEqual(metadata.extract_time('[alfen321][start]2018-08-28T13:14:45+0200'), '13:14:45+0200')

    def test_extract_time_list(self):
        data = ['[alfen321][start]2018-08-28T13:14:45+0200','[alfen321][end]2018-08-28T13:14:45+0200']
        res = ['13:14:45+0200', '13:14:45+0200']
        self.assertEqual(metadata.extract_time(data), res)

    def test_extract_timestamp_string(self):
        self.assertEqual(metadata.extract_timestamp('[alfen321][start]2018-08-28T13:14:45+0200'), '2018-08-28T13:14:45+0200')

    def test_seconds_to_timestamp(self):
        self.assertEqual(metadata.seconds_to_timestamp(10000), '2:46:40')

    def test_split_on_days(self):
        data = ['[davidcarl][start]2018-09-04T09:00:00+0200',
                '[davidcarl][end]2018-09-04T09:10:00+0200',
                '[davidcarl][start]2018-09-01T09:00:00+0200',
                '[davidcarl][end]2018-09-01T09:10:00+0200']
        res = defaultdict(list)
        res['2018-09-01'].append('[davidcarl][start]2018-09-01T09:00:00+0200')
        res['2018-09-01'].append('[davidcarl][end]2018-09-01T09:10:00+0200')
        res['2018-09-04'].append('[davidcarl][start]2018-09-04T09:00:00+0200')
        res['2018-09-04'].append('[davidcarl][end]2018-09-04T09:10:00+0200')
        self.assertEqual(metadata.split_on_days(data), res)

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

    def test_get_http_link(self):
        url = 'https://github.com/regebro/tzlocal.git'
        self.assertEqual(shared._get_http_link(url), 'https://www.github.com/regebro/tzlocal')

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
        
class Test_git_timestore(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        shared.set_quiet_mode(True)

    @classmethod
    def tearDownClass(self):
        shared.set_working_dir(os.getcwd())
        subprocess.call(['rm', '-rf', './test/test_env'], stdout=None, stderr=None)    

    def setUp(self):
        print(" In method", self._testMethodName)

    def test_simple_tests(self):
        subprocess.call(['bash', './test/scripts/Setup'], stdout=None, stderr=None)
        commits = subprocess.run(['bash', './test/scripts/get_commits'], stdout=subprocess.PIPE, encoding='utf-8').stdout.rstrip().split(' ')

        try:
            gtc.store()
        except:
            self.assertEqual(str(sys.exc_info()[1]), '1')

        #test commit first time and the commit arg    
        shared.set_working_dir('./test/test_env/clone1')
        content = {'user':'alfen', 'state':'start', 'timestamp':'2018-09-04T09:10:00+0200'}
        gtc.store(entry=content, commit=commits[0])
        timecommit_name = git_timestore.get_current_ref()
        self.assertTrue(timecommit_name is not None)
        expected = {commits[0]: {shared.sha1_gen_dict(content): content}}
        self.assertEqual(gtc.get_all_as_dict(), expected)

        #test push commit first time
        shared.set_working_dir('./test/test_env/clone1')
        gtc.push()
        shared.set_working_dir('./test/test_env/origin')
        timecommit_name = git_timestore.get_current_ref()
        self.assertTrue(timecommit_name is not None)
        content = {'user':'alfen', 'state':'start', 'timestamp':'2018-09-04T09:10:00+0200'}
        expected = {commits[0]: {shared.sha1_gen_dict(content): content}}
        self.assertEqual(gtc.get_all_as_dict(), expected)

        #test fetch first time no ref
        shared.set_working_dir('./test/test_env/clone2')
        gtc.fetch()
        timecommit_name = git_timestore.get_current_ref()
        self.assertTrue(timecommit_name is not None)
        content = {'user':'alfen', 'state':'start', 'timestamp':'2018-09-04T09:10:00+0200'}
        expected = {commits[0]: {shared.sha1_gen_dict(content): content}}
        self.assertEqual(gtc.get_all_as_dict(), expected)

        #test issue arg and next time commit
        shared.set_working_dir('./test/test_env/clone1')
        timecommit_name = git_timestore.get_current_ref()
        content = {'user':'alfen', 'state':'start', 'timestamp':'2018-09-04T09:15:00+0200'}
        gtc.store(entry=content, issue=4)
        #checking commit history
        old_timecommit_name = timecommit_name
        timecommit = git_timestore.load_git_commit_by_hash_name(git_timestore.get_current_ref())
        self.assertEqual(timecommit.parent, old_timecommit_name)
        #Check entries
        issue = git_timestore.save_git_blob(git_objects.Blob(os.getcwd()+'/test/test_env/origin/issue/4'))
        content1 = {'user':'alfen', 'state':'start', 'timestamp':'2018-09-04T09:15:00+0200'}     
        content2 = {'user':'alfen', 'state':'start', 'timestamp':'2018-09-04T09:10:00+0200'}        
        expected = {issue: {shared.sha1_gen_dict(content1): content1},\
                    commits[0]: {shared.sha1_gen_dict(content2): content2}}
        self.assertEqual(gtc.get_all_as_dict(), expected)

        # #test push with refs on origin        
        shared.set_working_dir('./test/test_env/origin')
        timecommit_name = git_timestore.get_current_ref()
        shared.set_working_dir('./test/test_env/clone1')
        gtc.push()
        shared.set_working_dir('./test/test_env/origin')
        #checking commit history
        old_timecommit_name = timecommit_name
        timecommit = git_timestore.load_git_commit_by_hash_name(git_timestore.get_current_ref())
        self.assertEqual(timecommit.parent, old_timecommit_name)
        #Check entries
        issue = git_timestore.save_git_blob(git_objects.Blob(os.getcwd()+'/test/test_env/origin/issue/4'))
        content1 = {'user':'alfen', 'state':'start', 'timestamp':'2018-09-04T09:15:00+0200'}     
        content2 = {'user':'alfen', 'state':'start', 'timestamp':'2018-09-04T09:10:00+0200'}        
        expected = {issue: {shared.sha1_gen_dict(content1): content1},\
                    commits[0]: {shared.sha1_gen_dict(content2): content2}}
        self.assertEqual(gtc.get_all_as_dict(), expected)

    def test_store_json(self):
        #setup test env
        subprocess.call(['bash', './test/scripts/Setup'], stdout=None, stderr=None)
        shared.set_working_dir('./test/test_env/clone2')
        json_obj = {'storage': {'repo': shared.get_gitpath(), 'issue':2}, 'content': {'user':'alfen', 'state':'start', 'timestamp':'2018-09-04T09:15:00+0200'}}        
        json_string = str(json_obj).replace('\'','"')
        gtc.store_json(json_string)
        issue2 = git_timestore.save_git_blob(git_objects.Blob(os.getcwd()+'/test/test_env/origin/issue/2'))
        expected = {issue2: {shared.sha1_gen_dict(json_obj['content']): json_obj['content']}}
        self.assertEqual(gtc.get_all_as_dict(), expected)

        expected = {shared.sha1_gen_dict(json_obj['content']): json_obj['content']}
        self.assertEqual(gtc.get_all_by_hash(issue2), expected)

        shared.set_working_dir('./test/test_env/clone1')
        json_obj = {'user':'alfen', 'state':'start', 'timestamp':'2018-09-04T09:15:00+0200'}        
        json_string = str(json_obj).replace('\'','"')        
        gtc.store(json=json_string, issue=2)
        issue2 = git_timestore.save_git_blob(git_objects.Blob(os.getcwd()+'/test/test_env/origin/issue/2')) 
        expected = {issue2: {shared.sha1_gen_dict(json_obj): json_obj}}
        self.assertEqual(gtc.get_all_as_dict(), expected)

        shared.set_working_dir('./test/test_env/clone1')
        os.remove(shared.get_gitpath() + 'refs/time/commits')
        json_obj = {'content':{'user':'alfen', 'state':'start', 'timestamp':'2018-09-04T09:15:00+0200'}}
        json_string = str(json_obj).replace('\'','"')      
        gtc.store(json=json_string, issue=2)
        issue2 = git_timestore.save_git_blob(git_objects.Blob(os.getcwd()+'/test/test_env/origin/issue/2')) 
        expected = {issue2: {shared.sha1_gen_dict(json_obj['content']): json_obj['content']}}
        self.assertEqual(gtc.get_all_as_dict(), expected)
        

    def test_merge_local_and_push(self):
        #setup test env
        subprocess.call(['bash', './test/scripts/Setup'], stdout=None, stderr=None)
        commits = subprocess.run(['bash', './test/scripts/get_commits'], stdout=subprocess.PIPE, encoding='utf-8').stdout.rstrip().split(' ')
        shared.set_working_dir('./test/test_env/clone1')
        content = {'user':'alfen', 'state':'start', 'timestamp':'2018-09-04T09:15:00+0200'}        
        gtc.store(entry=content, issue=4)
        gtc.push()

        #test of appending comment to allready exsisting blob
        shared.set_working_dir('./test/test_env/clone1')        
        content = {'user':'alfen', 'state':'end', 'timestamp':'2018-09-04T09:30:00+0200'}        
        gtc.store(entry=content, issue=4)
        #check tree
        timecommit_name = git_timestore.get_current_ref()
        commit = git_timestore.load_git_commit_by_hash_name(timecommit_name)
        tree = git_timestore.load_git_tree_by_hash_name(commit.get_tree())
        self.assertTrue(len(tree.get_all_entries()) is 1)
        #Check entries
        issue = git_timestore.save_git_blob(git_objects.Blob(os.getcwd()+'/test/test_env/origin/issue/4'))
        content1 = {'user':'alfen', 'state':'start', 'timestamp':'2018-09-04T09:15:00+0200'}        
        content2 = {'user':'alfen', 'state':'end', 'timestamp':'2018-09-04T09:30:00+0200'}                
        expected = {issue: {shared.sha1_gen_dict(content1): content1, shared.sha1_gen_dict(content2): content2}}
        self.assertEqual(gtc.get_all_as_dict(), expected)
        
        #push time on object that allready exist on origin
        shared.set_working_dir('./test/test_env/clone1')        
        gtc.push()
        shared.set_working_dir('./test/test_env/origin')
        #check tree
        timecommit_name = git_timestore.get_current_ref()
        commit = git_timestore.load_git_commit_by_hash_name(timecommit_name)
        tree = git_timestore.load_git_tree_by_hash_name(commit.get_tree())
        self.assertTrue(len(tree.get_all_entries()) is 1)
        #Check entries
        issue = git_timestore.save_git_blob(git_objects.Blob(os.getcwd()+'/test/test_env/origin/issue/4'))
        content1 = {'user':'alfen', 'state':'start', 'timestamp':'2018-09-04T09:15:00+0200'}        
        content2 = {'user':'alfen', 'state':'end', 'timestamp':'2018-09-04T09:30:00+0200'}                
        expected = {issue: {shared.sha1_gen_dict(content1): content1, shared.sha1_gen_dict(content2): content2}}
        self.assertEqual(gtc.get_all_as_dict(), expected)
        
    def test_merge_conflict_different_objects(self):
        #setup test env
        subprocess.call(['bash', './test/scripts/Setup'], stdout=None, stderr=None)
        commits = subprocess.run(['bash', './test/scripts/get_commits'], stdout=subprocess.PIPE, encoding='utf-8').stdout.rstrip().split(' ')
        
        shared.set_working_dir('./test/test_env/clone2')
        content = {'user':'david', 'state':'start', 'timestamp':'2018-09-04T09:30:00+0200'}        
        gtc.store(entry=content, issue=2)
        gtc.push()

        issue2 = git_timestore.save_git_blob(git_objects.Blob(os.getcwd()+'/test/test_env/origin/issue/2'))
        issue4 = git_timestore.save_git_blob(git_objects.Blob(os.getcwd()+'/test/test_env/origin/issue/4'))
        
        #test of comment to different blob
        shared.set_working_dir('./test/test_env/clone1')        
        content = {'user':'alfen', 'state':'start', 'timestamp':'2018-09-04T09:45:00+0200'}        
        gtc.store(entry=content, issue=4)
        gtc.push()
        #check tree
        timecommit_name = git_timestore.get_current_ref()
        commit = git_timestore.load_git_commit_by_hash_name(timecommit_name)
        tree = git_timestore.load_git_tree_by_hash_name(commit.get_tree())
        self.assertTrue(len(tree.get_all_entries()) is 2)
        #Check entries
        content1 = {'user':'david', 'state':'start', 'timestamp':'2018-09-04T09:30:00+0200'}                
        content2 = {'user':'alfen', 'state':'start', 'timestamp':'2018-09-04T09:45:00+0200'}        
        expected = {issue2: {shared.sha1_gen_dict(content1): content1}, issue4: {shared.sha1_gen_dict(content2): content2}}
        self.assertEqual(gtc.get_all_as_dict(), expected)
        
        #chek origin
        shared.set_working_dir('./test/test_env/origin')
        #check tree
        timecommit_name = git_timestore.get_current_ref()
        commit = git_timestore.load_git_commit_by_hash_name(timecommit_name)
        tree = git_timestore.load_git_tree_by_hash_name(commit.get_tree())
        self.assertTrue(len(tree.get_all_entries()) is 2)
        #Check entries
        content1 = {'user':'david', 'state':'start', 'timestamp':'2018-09-04T09:30:00+0200'}                
        content2 = {'user':'alfen', 'state':'start', 'timestamp':'2018-09-04T09:45:00+0200'}        
        expected = {issue2: {shared.sha1_gen_dict(content1): content1}, issue4: {shared.sha1_gen_dict(content2): content2}}
        self.assertEqual(gtc.get_all_as_dict(), expected)
        
    def test_merge_fetch_conflict_different_objects(self):
        #setup test env
        subprocess.call(['bash', './test/scripts/Setup'], stdout=None, stderr=None)
        commits = subprocess.run(['bash', './test/scripts/get_commits'], stdout=subprocess.PIPE, encoding='utf-8').stdout.rstrip().split(' ')
        shared.set_working_dir('./test/test_env/clone2')
        content = {'user':'david', 'state':'start', 'timestamp':'2018-09-04T09:30:00+0200'}        
        gtc.store(entry=content, issue=2)
        gtc.push()

        issue2 = git_timestore.save_git_blob(git_objects.Blob(os.getcwd()+'/test/test_env/origin/issue/2'))
        issue4 = git_timestore.save_git_blob(git_objects.Blob(os.getcwd()+'/test/test_env/origin/issue/4'))
        
        #test of comment to different blob
        shared.set_working_dir('./test/test_env/clone1')        
        content = {'user':'alfen', 'state':'start', 'timestamp':'2018-09-04T09:45:00+0200'}        
        gtc.store(entry=content, issue=4)
        gtc.fetch()
        #check tree
        timecommit_name = git_timestore.get_current_ref()
        commit = git_timestore.load_git_commit_by_hash_name(timecommit_name)
        tree = git_timestore.load_git_tree_by_hash_name(commit.get_tree())
        self.assertTrue(len(tree.get_all_entries()) is 2)
        #Check entries
        content1 = {'user':'david', 'state':'start', 'timestamp':'2018-09-04T09:30:00+0200'}                
        content2 = {'user':'alfen', 'state':'start', 'timestamp':'2018-09-04T09:45:00+0200'}        
        expected = {issue2: {shared.sha1_gen_dict(content1): content1}, issue4: {shared.sha1_gen_dict(content2): content2}}
        self.assertEqual(gtc.get_all_as_dict(), expected)
        
        #chek origin
        shared.set_working_dir('./test/test_env/origin')
        #check tree
        timecommit_name = git_timestore.get_current_ref()
        commit = git_timestore.load_git_commit_by_hash_name(timecommit_name)
        tree = git_timestore.load_git_tree_by_hash_name(commit.get_tree())
        self.assertTrue(len(tree.get_all_entries()) is 1)
        #Check entries expect not to have clone1 changes    
        content1 = {'user':'david', 'state':'start', 'timestamp':'2018-09-04T09:30:00+0200'}                
        expected = {issue2: {shared.sha1_gen_dict(content1): content1}}
        self.assertEqual(gtc.get_all_as_dict(), expected)

    def test_merge_conflict_same_objects(self):
        #setup test env
        subprocess.call(['bash', './test/scripts/Setup'], stdout=None, stderr=None)
        commits = subprocess.run(['bash', './test/scripts/get_commits'], stdout=subprocess.PIPE, encoding='utf-8').stdout.rstrip().split(' ')
        shared.set_working_dir('./test/test_env/clone2')
        content = {'user':'alfen', 'state':'start', 'timestamp':'2018-09-04T09:45:00+0200'}        
        gtc.store(entry=content, issue=4)
        gtc.push()

        issue4 = git_timestore.save_git_blob(git_objects.Blob(os.getcwd()+'/test/test_env/origin/issue/4'))
        
        #test of appending comment to allready exsisting blob
        shared.set_working_dir('./test/test_env/clone1')        
        content = {'user':'david', 'state':'start', 'timestamp':'2018-09-04T09:55:00+0200'}        
        gtc.store(entry=content, issue=4)
        gtc.push()
        #check tree
        timecommit_name = git_timestore.get_current_ref()
        commit = git_timestore.load_git_commit_by_hash_name(timecommit_name)
        tree = git_timestore.load_git_tree_by_hash_name(commit.get_tree())
        self.assertTrue(len(tree.get_all_entries()) is 1)
        #Check entries
        content1 = {'user':'alfen', 'state':'start', 'timestamp':'2018-09-04T09:45:00+0200'}        
        content2 = {'user':'david', 'state':'start', 'timestamp':'2018-09-04T09:55:00+0200'}        
        expected = {issue4: {shared.sha1_gen_dict(content1): content1, shared.sha1_gen_dict(content2): content2}}
        self.assertEqual(gtc.get_all_as_dict(), expected)
        
        #chek origin
        shared.set_working_dir('./test/test_env/origin')
        #check tree
        timecommit_name = git_timestore.get_current_ref()
        commit = git_timestore.load_git_commit_by_hash_name(timecommit_name)
        tree = git_timestore.load_git_tree_by_hash_name(commit.get_tree())
        self.assertTrue(len(tree.get_all_entries()) is 1)
        #Check entries
        content1 = {'user':'alfen', 'state':'start', 'timestamp':'2018-09-04T09:45:00+0200'}        
        content2 = {'user':'david', 'state':'start', 'timestamp':'2018-09-04T09:55:00+0200'}        
        expected = {issue4: {shared.sha1_gen_dict(content1): content1, shared.sha1_gen_dict(content2): content2}}
        self.assertEqual(gtc.get_all_as_dict(), expected)

    def test_merge_conflict_same_objects_with_history(self):
        #setup test env
        subprocess.call(['bash', './test/scripts/Setup'], stdout=None, stderr=None)
        commits = subprocess.run(['bash', './test/scripts/get_commits'], stdout=subprocess.PIPE, encoding='utf-8').stdout.rstrip().split(' ')
        shared.set_working_dir('./test/test_env/clone2')
        content = {'user':'david', 'state':'start', 'timestamp':'2018-09-04T09:55:00+0200'}        
        gtc.store(entry=content, issue=4)
        gtc.push()
        shared.set_working_dir('./test/test_env/clone1')
        gtc.fetch()
        shared.set_working_dir('./test/test_env/clone2')
        content = {'user':'david', 'state':'end', 'timestamp':'2018-09-04T10:55:00+0200'}        
        gtc.store(entry=content, issue=4)
        gtc.push()
        
        issue4 = git_timestore.save_git_blob(git_objects.Blob(os.getcwd()+'/test/test_env/origin/issue/4'))
        
        #test of appending comment to allready exsisting blob
        shared.set_working_dir('./test/test_env/clone1')        
        content = {'user':'alfen', 'state':'start', 'timestamp':'2018-09-04T11:55:00+0200'}        
        gtc.store(entry=content, issue=4)
        gtc.push()
        #check tree
        timecommit_name = git_timestore.get_current_ref()
        commit = git_timestore.load_git_commit_by_hash_name(timecommit_name)
        tree = git_timestore.load_git_tree_by_hash_name(commit.get_tree())
        self.assertTrue(len(tree.get_all_entries()) is 1)
        #Check entries
        content1 = {'user':'david', 'state':'start', 'timestamp':'2018-09-04T09:55:00+0200'}        
        content2 = {'user':'david', 'state':'end', 'timestamp':'2018-09-04T10:55:00+0200'}        
        content3 = {'user':'alfen', 'state':'start', 'timestamp':'2018-09-04T11:55:00+0200'}        
        expected = {issue4: {shared.sha1_gen_dict(content1): content1, 
                             shared.sha1_gen_dict(content2): content2, 
                             shared.sha1_gen_dict(content3): content3}}
        self.assertEqual(gtc.get_all_as_dict(), expected)
        
        #chek origin
        shared.set_working_dir('./test/test_env/origin')
        #check tree
        timecommit_name = git_timestore.get_current_ref()
        commit = git_timestore.load_git_commit_by_hash_name(timecommit_name)
        tree = git_timestore.load_git_tree_by_hash_name(commit.get_tree())
        self.assertTrue(len(tree.get_all_entries()) is 1)
        #Check entries
        content1 = {'user':'david', 'state':'start', 'timestamp':'2018-09-04T09:55:00+0200'}        
        content2 = {'user':'david', 'state':'end', 'timestamp':'2018-09-04T10:55:00+0200'}        
        content3 = {'user':'alfen', 'state':'start', 'timestamp':'2018-09-04T11:55:00+0200'}        
        expected = {issue4: {shared.sha1_gen_dict(content1): content1, 
                             shared.sha1_gen_dict(content2): content2, 
                             shared.sha1_gen_dict(content3): content3}}
        self.assertEqual(gtc.get_all_as_dict(), expected)
        

if __name__ == '__main__':
    unittest.main()