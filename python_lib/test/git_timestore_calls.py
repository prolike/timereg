import unittest, subprocess, os, sys
from python_lib import shared, git_timestore, git_timestore_calls as gtc, git_objects, settings


class Test_git_timestore(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        shared.set_quiet_mode(True)
        settings.settings['autopush'] = 'False'

    @classmethod
    def tearDownClass(self):
        shared.set_working_dir(os.getcwd())
        subprocess.call(['rm', '-rf', './test/test_env'],
                        stdout=None, stderr=None)

    def setUp(self):
        print(" In method", self._testMethodName)

    def test_simple_tests(self):
        subprocess.call(['bash', './test/scripts/Setup'],
                        stdout=None, stderr=None)
        commits = subprocess.run(['bash', './test/scripts/get_commits'],
                                 stdout=subprocess.PIPE, encoding='utf-8').stdout.rstrip().split(' ')

        try:
            gtc.store()
        except:
            self.assertEqual(str(sys.exc_info()[1]), '1')

        # test commit first time and the commit arg
        shared.set_working_dir('./test/test_env/clone1')
        content = {'user': 'alfen', 'state': 'start',
                   'timestamp': '2018-09-04T09:10:00+0200'}
        gtc.store(entry=content, commit=commits[0])
        timecommit_name = git_timestore.get_current_ref()
        self.assertTrue(timecommit_name is not None)
        expected = {commits[0]: {shared.sha1_gen_dict(content): content}}
        self.assertEqual(gtc.get_all_as_dict(), expected)

        # test push commit first time
        shared.set_working_dir('./test/test_env/clone1')
        gtc.push()
        shared.set_working_dir('./test/test_env/origin')
        timecommit_name = git_timestore.get_current_ref()
        self.assertTrue(timecommit_name is not None)
        content = {'user': 'alfen', 'state': 'start',
                   'timestamp': '2018-09-04T09:10:00+0200'}
        expected = {commits[0]: {shared.sha1_gen_dict(content): content}}
        self.assertEqual(gtc.get_all_as_dict(), expected)

        # test fetch first time no ref
        shared.set_working_dir('./test/test_env/clone2')
        gtc.fetch()
        timecommit_name = git_timestore.get_current_ref()
        self.assertTrue(timecommit_name is not None)
        content = {'user': 'alfen', 'state': 'start',
                   'timestamp': '2018-09-04T09:10:00+0200'}
        expected = {commits[0]: {shared.sha1_gen_dict(content): content}}
        self.assertEqual(gtc.get_all_as_dict(), expected)

        # test issue arg and next time commit
        shared.set_working_dir('./test/test_env/clone1')
        timecommit_name = git_timestore.get_current_ref()
        content = {'user': 'alfen', 'state': 'start',
                   'timestamp': '2018-09-04T09:15:00+0200'}
        gtc.store(entry=content, issue=4)
        # checking commit history
        old_timecommit_name = timecommit_name
        timecommit = git_timestore.load_git_commit_by_hash(
            git_timestore.get_current_ref())
        self.assertEqual(timecommit.parent, old_timecommit_name)
        # Check entries
        issue = git_timestore.save_git_blob(git_objects.Blob(
            os.getcwd()+'/test/test_env/origin/issue/4'))
        content1 = {'user': 'alfen', 'state': 'start',
                    'timestamp': '2018-09-04T09:15:00+0200'}
        content2 = {'user': 'alfen', 'state': 'start',
                    'timestamp': '2018-09-04T09:10:00+0200'}
        expected = {issue: {shared.sha1_gen_dict(content1): content1},
                    commits[0]: {shared.sha1_gen_dict(content2): content2}}
        self.assertEqual(gtc.get_all_as_dict(), expected)

        # #test push with refs on origin        
        shared.set_working_dir('./test/test_env/origin')
        timecommit_name = git_timestore.get_current_ref()
        shared.set_working_dir('./test/test_env/clone1')
        gtc.push()
        shared.set_working_dir('./test/test_env/origin')
        # checking commit history
        old_timecommit_name = timecommit_name
        timecommit = git_timestore.load_git_commit_by_hash(
            git_timestore.get_current_ref())
        self.assertEqual(timecommit.parent, old_timecommit_name)
        # Check entries
        issue = git_timestore.save_git_blob(git_objects.Blob(
            os.getcwd()+'/test/test_env/origin/issue/4'))
        content1 = {'user': 'alfen', 'state': 'start',
                    'timestamp': '2018-09-04T09:15:00+0200'}
        content2 = {'user': 'alfen', 'state': 'start',
                    'timestamp': '2018-09-04T09:10:00+0200'}
        expected = {issue: {shared.sha1_gen_dict(content1): content1},
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
        # setup test env
        subprocess.call(['bash', './test/scripts/Setup'],
                        stdout=None, stderr=None)
        commits = subprocess.run(['bash', './test/scripts/get_commits'],
                                 stdout=subprocess.PIPE, encoding='utf-8').stdout.rstrip().split(' ')
        shared.set_working_dir('./test/test_env/clone1')
        content = {'user': 'alfen', 'state': 'start',
                   'timestamp': '2018-09-04T09:15:00+0200'}
        gtc.store(entry=content, issue=4)
        gtc.push()

        # test of appending comment to allready exsisting blob
        shared.set_working_dir('./test/test_env/clone1')
        content = {'user': 'alfen', 'state': 'end',
                   'timestamp': '2018-09-04T09:30:00+0200'}
        gtc.store(entry=content, issue=4)
        # check tree
        timecommit_name = git_timestore.get_current_ref()
        commit = git_timestore.load_git_commit_by_hash(timecommit_name)
        tree = git_timestore.load_git_tree_by_hash(commit.get_tree())
        self.assertTrue(len(tree.get_all_entries()) is 1)
        # Check entries
        issue = git_timestore.save_git_blob(git_objects.Blob(
            os.getcwd()+'/test/test_env/origin/issue/4'))
        content1 = {'user': 'alfen', 'state': 'start',
                    'timestamp': '2018-09-04T09:15:00+0200'}
        content2 = {'user': 'alfen', 'state': 'end',
                    'timestamp': '2018-09-04T09:30:00+0200'}
        expected = {issue: {shared.sha1_gen_dict(
            content1): content1, shared.sha1_gen_dict(content2): content2}}
        self.assertEqual(gtc.get_all_as_dict(), expected)

        # push time on object that allready exist on origin
        shared.set_working_dir('./test/test_env/clone1')
        gtc.push()
        shared.set_working_dir('./test/test_env/origin')
        # check tree
        timecommit_name = git_timestore.get_current_ref()
        commit = git_timestore.load_git_commit_by_hash(timecommit_name)
        tree = git_timestore.load_git_tree_by_hash(commit.get_tree())
        self.assertTrue(len(tree.get_all_entries()) is 1)
        # Check entries
        issue = git_timestore.save_git_blob(git_objects.Blob(
            os.getcwd()+'/test/test_env/origin/issue/4'))
        content1 = {'user': 'alfen', 'state': 'start',
                    'timestamp': '2018-09-04T09:15:00+0200'}
        content2 = {'user': 'alfen', 'state': 'end',
                    'timestamp': '2018-09-04T09:30:00+0200'}
        expected = {issue: {shared.sha1_gen_dict(
            content1): content1, shared.sha1_gen_dict(content2): content2}}
        self.assertEqual(gtc.get_all_as_dict(), expected)

    def test_merge_conflict_different_objects(self):
        # setup test env
        subprocess.call(['bash', './test/scripts/Setup'],
                        stdout=None, stderr=None)
        commits = subprocess.run(['bash', './test/scripts/get_commits'],
                                 stdout=subprocess.PIPE, encoding='utf-8').stdout.rstrip().split(' ')

        shared.set_working_dir('./test/test_env/clone2')
        content = {'user': 'david', 'state': 'start',
                   'timestamp': '2018-09-04T09:30:00+0200'}
        gtc.store(entry=content, issue=2)
        gtc.push()

        issue2 = git_timestore.save_git_blob(git_objects.Blob(
            os.getcwd()+'/test/test_env/origin/issue/2'))
        issue4 = git_timestore.save_git_blob(git_objects.Blob(
            os.getcwd()+'/test/test_env/origin/issue/4'))

        # test of comment to different blob
        shared.set_working_dir('./test/test_env/clone1')
        content = {'user': 'alfen', 'state': 'start',
                   'timestamp': '2018-09-04T09:45:00+0200'}
        gtc.store(entry=content, issue=4)
        gtc.push()
        # check tree
        timecommit_name = git_timestore.get_current_ref()
        commit = git_timestore.load_git_commit_by_hash(timecommit_name)
        tree = git_timestore.load_git_tree_by_hash(commit.get_tree())
        self.assertTrue(len(tree.get_all_entries()) is 2)
        # Check entries
        content1 = {'user': 'david', 'state': 'start',
                    'timestamp': '2018-09-04T09:30:00+0200'}
        content2 = {'user': 'alfen', 'state': 'start',
                    'timestamp': '2018-09-04T09:45:00+0200'}
        expected = {issue2: {shared.sha1_gen_dict(content1): content1}, issue4: {
            shared.sha1_gen_dict(content2): content2}}
        self.assertEqual(gtc.get_all_as_dict(), expected)

        # chek origin
        shared.set_working_dir('./test/test_env/origin')
        # check tree
        timecommit_name = git_timestore.get_current_ref()
        commit = git_timestore.load_git_commit_by_hash(timecommit_name)
        tree = git_timestore.load_git_tree_by_hash(commit.get_tree())
        self.assertTrue(len(tree.get_all_entries()) is 2)
        # Check entries
        content1 = {'user': 'david', 'state': 'start',
                    'timestamp': '2018-09-04T09:30:00+0200'}
        content2 = {'user': 'alfen', 'state': 'start',
                    'timestamp': '2018-09-04T09:45:00+0200'}
        expected = {issue2: {shared.sha1_gen_dict(content1): content1}, issue4: {
            shared.sha1_gen_dict(content2): content2}}
        self.assertEqual(gtc.get_all_as_dict(), expected)

    def test_merge_fetch_conflict_different_objects(self):
        # setup test env
        subprocess.call(['bash', './test/scripts/Setup'],
                        stdout=None, stderr=None)
        commits = subprocess.run(['bash', './test/scripts/get_commits'],
                                 stdout=subprocess.PIPE, encoding='utf-8').stdout.rstrip().split(' ')
        shared.set_working_dir('./test/test_env/clone2')
        content = {'user': 'david', 'state': 'start',
                   'timestamp': '2018-09-04T09:30:00+0200'}
        gtc.store(entry=content, issue=2)
        gtc.push()

        issue2 = git_timestore.save_git_blob(git_objects.Blob(
            os.getcwd()+'/test/test_env/origin/issue/2'))
        issue4 = git_timestore.save_git_blob(git_objects.Blob(
            os.getcwd()+'/test/test_env/origin/issue/4'))

        # test of comment to different blob
        shared.set_working_dir('./test/test_env/clone1')
        content = {'user': 'alfen', 'state': 'start',
                   'timestamp': '2018-09-04T09:45:00+0200'}
        gtc.store(entry=content, issue=4)
        gtc.fetch()
        # check tree
        timecommit_name = git_timestore.get_current_ref()
        commit = git_timestore.load_git_commit_by_hash(timecommit_name)
        tree = git_timestore.load_git_tree_by_hash(commit.get_tree())
        self.assertTrue(len(tree.get_all_entries()) is 2)
        # Check entries
        content1 = {'user': 'david', 'state': 'start',
                    'timestamp': '2018-09-04T09:30:00+0200'}
        content2 = {'user': 'alfen', 'state': 'start',
                    'timestamp': '2018-09-04T09:45:00+0200'}
        expected = {issue2: {shared.sha1_gen_dict(content1): content1}, issue4: {
            shared.sha1_gen_dict(content2): content2}}
        self.assertEqual(gtc.get_all_as_dict(), expected)

        # chek origin
        shared.set_working_dir('./test/test_env/origin')
        # check tree
        timecommit_name = git_timestore.get_current_ref()
        commit = git_timestore.load_git_commit_by_hash(timecommit_name)
        tree = git_timestore.load_git_tree_by_hash(commit.get_tree())
        self.assertTrue(len(tree.get_all_entries()) is 1)
        # Check entries expect not to have clone1 changes
        content1 = {'user': 'david', 'state': 'start',
                    'timestamp': '2018-09-04T09:30:00+0200'}
        expected = {issue2: {shared.sha1_gen_dict(content1): content1}}
        self.assertEqual(gtc.get_all_as_dict(), expected)

    def test_merge_conflict_same_objects(self):
        # setup test env
        subprocess.call(['bash', './test/scripts/Setup'],
                        stdout=None, stderr=None)
        commits = subprocess.run(['bash', './test/scripts/get_commits'],
                                 stdout=subprocess.PIPE, encoding='utf-8').stdout.rstrip().split(' ')
        shared.set_working_dir('./test/test_env/clone2')
        content = {'user': 'alfen', 'state': 'start',
                   'timestamp': '2018-09-04T09:45:00+0200'}
        gtc.store(entry=content, issue=4)
        gtc.push()

        issue4 = git_timestore.save_git_blob(git_objects.Blob(
            os.getcwd()+'/test/test_env/origin/issue/4'))

        # test of appending comment to allready exsisting blob
        shared.set_working_dir('./test/test_env/clone1')
        content = {'user': 'david', 'state': 'start',
                   'timestamp': '2018-09-04T09:55:00+0200'}
        gtc.store(entry=content, issue=4)
        gtc.push()
        # check tree
        timecommit_name = git_timestore.get_current_ref()
        commit = git_timestore.load_git_commit_by_hash(timecommit_name)
        tree = git_timestore.load_git_tree_by_hash(commit.get_tree())
        self.assertTrue(len(tree.get_all_entries()) is 1)
        # Check entries
        content1 = {'user': 'alfen', 'state': 'start',
                    'timestamp': '2018-09-04T09:45:00+0200'}
        content2 = {'user': 'david', 'state': 'start',
                    'timestamp': '2018-09-04T09:55:00+0200'}
        expected = {issue4: {shared.sha1_gen_dict(
            content1): content1, shared.sha1_gen_dict(content2): content2}}
        self.assertEqual(gtc.get_all_as_dict(), expected)

        # chek origin
        shared.set_working_dir('./test/test_env/origin')
        # check tree
        timecommit_name = git_timestore.get_current_ref()
        commit = git_timestore.load_git_commit_by_hash(timecommit_name)
        tree = git_timestore.load_git_tree_by_hash(commit.get_tree())
        self.assertTrue(len(tree.get_all_entries()) is 1)
        # Check entries
        content1 = {'user': 'alfen', 'state': 'start',
                    'timestamp': '2018-09-04T09:45:00+0200'}
        content2 = {'user': 'david', 'state': 'start',
                    'timestamp': '2018-09-04T09:55:00+0200'}
        expected = {issue4: {shared.sha1_gen_dict(
            content1): content1, shared.sha1_gen_dict(content2): content2}}
        self.assertEqual(gtc.get_all_as_dict(), expected)

    def test_merge_conflict_same_objects_with_history(self):
        # setup test env
        subprocess.call(['bash', './test/scripts/Setup'],
                        stdout=None, stderr=None)
        commits = subprocess.run(['bash', './test/scripts/get_commits'],
                                 stdout=subprocess.PIPE, encoding='utf-8').stdout.rstrip().split(' ')
        shared.set_working_dir('./test/test_env/clone2')
        content = {'user': 'david', 'state': 'start',
                   'timestamp': '2018-09-04T09:55:00+0200'}
        gtc.store(entry=content, issue=4)
        gtc.push()
        shared.set_working_dir('./test/test_env/clone1')
        gtc.fetch()
        shared.set_working_dir('./test/test_env/clone2')
        content = {'user': 'david', 'state': 'end',
                   'timestamp': '2018-09-04T10:55:00+0200'}
        gtc.store(entry=content, issue=4)
        gtc.push()

        issue4 = git_timestore.save_git_blob(git_objects.Blob(
            os.getcwd()+'/test/test_env/origin/issue/4'))

        # test of appending comment to allready exsisting blob
        shared.set_working_dir('./test/test_env/clone1')
        content = {'user': 'alfen', 'state': 'start',
                   'timestamp': '2018-09-04T11:55:00+0200'}
        gtc.store(entry=content, issue=4)
        gtc.push()
        # check tree
        timecommit_name = git_timestore.get_current_ref()
        commit = git_timestore.load_git_commit_by_hash(timecommit_name)
        tree = git_timestore.load_git_tree_by_hash(commit.get_tree())
        self.assertTrue(len(tree.get_all_entries()) is 1)
        # Check entries
        content1 = {'user': 'david', 'state': 'start',
                    'timestamp': '2018-09-04T09:55:00+0200'}
        content2 = {'user': 'david', 'state': 'end',
                    'timestamp': '2018-09-04T10:55:00+0200'}
        content3 = {'user': 'alfen', 'state': 'start',
                    'timestamp': '2018-09-04T11:55:00+0200'}
        expected = {issue4: {shared.sha1_gen_dict(content1): content1,
                             shared.sha1_gen_dict(content2): content2,
                             shared.sha1_gen_dict(content3): content3}}
        self.assertEqual(gtc.get_all_as_dict(), expected)

        # chek origin
        shared.set_working_dir('./test/test_env/origin')
        # check tree
        timecommit_name = git_timestore.get_current_ref()
        commit = git_timestore.load_git_commit_by_hash(timecommit_name)
        tree = git_timestore.load_git_tree_by_hash(commit.get_tree())
        self.assertTrue(len(tree.get_all_entries()) is 1)
        # Check entries
        content1 = {'user': 'david', 'state': 'start',
                    'timestamp': '2018-09-04T09:55:00+0200'}
        content2 = {'user': 'david', 'state': 'end',
                    'timestamp': '2018-09-04T10:55:00+0200'}
        content3 = {'user': 'alfen', 'state': 'start',
                    'timestamp': '2018-09-04T11:55:00+0200'}
        expected = {issue4: {shared.sha1_gen_dict(content1): content1,
                             shared.sha1_gen_dict(content2): content2,
                             shared.sha1_gen_dict(content3): content3}}
        self.assertEqual(gtc.get_all_as_dict(), expected)
