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

    def test_simple(self):
        subprocess.call(['bash', './test/scripts/Setup'],
                        stdout=None, stderr=None)
        try:
            gtc.store()
        except:
            self.assertEqual(str(sys.exc_info()[1]), '1')

        # test commit first time direct to file
        shared.set_working_dir('./test/test_env/clone1')
        content = {'user': 'alfen', 'something': 'some data'}
        place = ['abc']
        gtc.store(target=place, content=content)
        timecommit_name = git_timestore.get_current_ref('refs/time/commits')
        self.assertTrue(timecommit_name is not None)
        expected = {shared.sha1_gen_dict(content): content}
        self.assertEqual(gtc.get_all_by_path(place), expected)
        
        #test with advance path
        shared.set_working_dir('./test/test_env/clone1')
        content = {'user': 'alfen', 'something': 'some data'}
        place = ['asd','dada']
        gtc.store(target=place, content=content)
        timecommit_name = git_timestore.get_current_ref('refs/time/commits')
        self.assertTrue(timecommit_name is not None)
        expected = {shared.sha1_gen_dict(content): content}
        self.assertEqual(gtc.get_all_by_path(place), expected)

        # test push commit first time
        shared.set_working_dir('./test/test_env/clone1')
        gtc.push()
        shared.set_working_dir('./test/test_env/origin')
        timecommit_name = git_timestore.get_current_ref('refs/time/commits')
        self.assertTrue(timecommit_name is not None)
        content = {'user': 'alfen', 'something': 'some data'}
        place = ['abc']
        expected = {shared.sha1_gen_dict(content): content}
        self.assertEqual(gtc.get_all_by_path(place), expected)
        
        content = {'user': 'alfen', 'something': 'some data'}
        place = ['asd','dada']
        expected = {shared.sha1_gen_dict(content): content}
        self.assertEqual(gtc.get_all_by_path(place), expected)
        
        # test fetch first time no ref
        shared.set_working_dir('./test/test_env/clone2')
        gtc.fetch()
        timecommit_name = git_timestore.get_current_ref('refs/time/commits')
        self.assertTrue(timecommit_name is not None)
        content = {'user': 'alfen', 'something': 'some data'}
        place = ['abc']
        expected = {shared.sha1_gen_dict(content): content}
        self.assertEqual(gtc.get_all_by_path(place), expected)
        
        content = {'user': 'alfen', 'something': 'some data'}
        place = ['asd','dada']
        expected = {shared.sha1_gen_dict(content): content}
        self.assertEqual(gtc.get_all_by_path(place), expected)


    def test_submit_to_existing_path(self):
        subprocess.call(['bash', './test/scripts/Setup'],
                        stdout=None, stderr=None)

        shared.set_working_dir('./test/test_env/clone1')
        content1 = {'user': 'alfen', 'something': 'some data'}
        place = ['asd','dada']
        gtc.store(target=place, content=content1)
        gtc.push()
        content2 = {'user': 'alfen', 'something': 'some other data'}
        gtc.store(target=place, content=content2)
        gtc.push()
        timecommit_name = git_timestore.get_current_ref('refs/time/commits')
        self.assertTrue(timecommit_name is not None)
        expected = {shared.sha1_gen_dict(content1): content1, shared.sha1_gen_dict(content2): content2}
        self.assertEqual(gtc.get_all_by_path(place), expected)

        shared.set_working_dir('./test/test_env/origin')
        timecommit_name = git_timestore.get_current_ref('refs/time/commits')
        self.assertTrue(timecommit_name is not None)
        expected = {shared.sha1_gen_dict(content1): content1, shared.sha1_gen_dict(content2): content2}
        self.assertEqual(gtc.get_all_by_path(place), expected)

        #test append
        shared.set_working_dir('./test/test_env/clone1')
        place = ['asd','dada']
        append = shared.sha1_gen_dict(content1)
        append_data = {'more':'data'}
        gtc.store(target=place, append=append, content=append_data)
        content1.update(append_data)
        timecommit_name = git_timestore.get_current_ref('refs/time/commits')
        self.assertTrue(timecommit_name is not None)
        expected = {shared.sha1_gen_dict(content1): content1, shared.sha1_gen_dict(content2): content2}
        self.assertEqual(gtc.get_all_by_path(place), expected)

        #test remove
        place = ['asd','dada']
        remove = shared.sha1_gen_dict(content2)
        gtc.store(target=place, remove=remove)
        timecommit_name = git_timestore.get_current_ref('refs/time/commits')
        self.assertTrue(timecommit_name is not None)
        expected = {shared.sha1_gen_dict(content1): content1}
        self.assertEqual(gtc.get_all_by_path(place), expected)


    
    def test_merge_conflict_simple_ref_merge(self):
        # setup test env
        subprocess.call(['bash', './test/scripts/Setup'],
                        stdout=None, stderr=None)
        shared.set_working_dir('./test/test_env/clone1')
        content1 = {'user': 'alfen', 'something': 'some data'}
        place1 = ['asd','dada']
        gtc.store(target=place1, content=content1)
        gtc.push()
    
        # merge different path no history
        shared.set_working_dir('./test/test_env/clone2')
        content2 = {'user': 'alfen', 'something': 'some data'}
        place2 = ['cvb','dada']
        gtc.store(target=place2, content=content2)
        gtc.push()

        timecommit_name = git_timestore.get_current_ref('refs/time/commits')
        self.assertTrue(timecommit_name is not None)
        expected = {shared.sha1_gen_dict(content1): content1}
        self.assertEqual(gtc.get_all_by_path(place1), expected)
        expected = {shared.sha1_gen_dict(content2): content2}
        self.assertEqual(gtc.get_all_by_path(place2), expected)

        shared.set_working_dir('./test/test_env/origin')
        timecommit_name = git_timestore.get_current_ref('refs/time/commits')
        self.assertTrue(timecommit_name is not None)
        expected = {shared.sha1_gen_dict(content1): content1}
        self.assertEqual(gtc.get_all_by_path(place1), expected)
        expected = {shared.sha1_gen_dict(content2): content2}
        self.assertEqual(gtc.get_all_by_path(place2), expected)

        # merge different path with history
        shared.set_working_dir('./test/test_env/clone1')
        content3 = {'user': 'alfen', 'something': 'some data'}
        place3 = ['asd','dada2']
        gtc.store(target=place3, content=content3)
        gtc.fetch()
        gtc.push()
        timecommit_name = git_timestore.get_current_ref('refs/time/commits')
        self.assertTrue(timecommit_name is not None)
        expected = {shared.sha1_gen_dict(content1): content1}
        self.assertEqual(gtc.get_all_by_path(place1), expected)
        expected = {shared.sha1_gen_dict(content2): content2}
        self.assertEqual(gtc.get_all_by_path(place2), expected)
        expected = {shared.sha1_gen_dict(content3): content3}
        self.assertEqual(gtc.get_all_by_path(place3), expected)

        shared.set_working_dir('./test/test_env/origin')
        timecommit_name = git_timestore.get_current_ref('refs/time/commits')
        self.assertTrue(timecommit_name is not None)
        expected = {shared.sha1_gen_dict(content1): content1}
        self.assertEqual(gtc.get_all_by_path(place1), expected)
        expected = {shared.sha1_gen_dict(content2): content2}
        self.assertEqual(gtc.get_all_by_path(place2), expected)
        expected = {shared.sha1_gen_dict(content3): content3}
        self.assertEqual(gtc.get_all_by_path(place3), expected)

    def test_merge_conflict_same_path(self):
        # setup test env
        subprocess.call(['bash', './test/scripts/Setup'],
                        stdout=None, stderr=None)
        shared.set_working_dir('./test/test_env/clone1')
        content1 = {'user': 'alfen', 'something': 'some data'}
        place1 = ['asd','dada']
        gtc.store(target=place1, content=content1)
        gtc.push()
    
        # merge conflict same path no history
        shared.set_working_dir('./test/test_env/clone2')
        content2 = {'user': 'alfen', 'something': 'some other data'}
        gtc.store(target=place1, content=content2)
        gtc.push()
        
        timecommit_name = git_timestore.get_current_ref('refs/time/commits')
        self.assertTrue(timecommit_name is not None)
        expected = {shared.sha1_gen_dict(content1): content1, \
                    shared.sha1_gen_dict(content2): content2}
        self.assertEqual(gtc.get_all_by_path(place1), expected)
        
        shared.set_working_dir('./test/test_env/origin')
        timecommit_name = git_timestore.get_current_ref('refs/time/commits')
        self.assertTrue(timecommit_name is not None)
        expected = {shared.sha1_gen_dict(content1): content1, \
                    shared.sha1_gen_dict(content2): content2}
        self.assertEqual(gtc.get_all_by_path(place1), expected)

        #merge conflict same path with history
        shared.set_working_dir('./test/test_env/clone1')
        content3 = {'user': 'alfen', 'something': 'some data new data'}
        gtc.store(target=place1, content=content3)
        gtc.push()
        timecommit_name = git_timestore.get_current_ref('refs/time/commits')
        self.assertTrue(timecommit_name is not None)
        expected = {shared.sha1_gen_dict(content1): content1, \
                    shared.sha1_gen_dict(content2): content2, \
                    shared.sha1_gen_dict(content3): content3}
        self.assertEqual(gtc.get_all_by_path(place1), expected)
