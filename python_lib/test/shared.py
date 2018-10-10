import unittest, os
from python_lib import shared


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
        expected = '/'.join(os.getcwd().split('/')
                            [:-2]) + '/home/usr/Documents'
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
        self.assertEqual(shared._get_http_link(
            url), 'https://www.github.com/regebro/tzlocal')

    def test_listsplitter(self):
        testdata = {'2df195ddc6fd9153a2326ce55a718455ca5e79bc': {'ce31b3b3492cae01018f2859b87d69a840b15fb5': {'user': 'davidcarl', 'state': 'start', 'timestamp': '2018-09-25T08:06:00+0200', 'storage': {'issuehash': '2df195ddc6fd9153a2326ce55a718455ca5e79bc', 'linehash': 'ce31b3b3492cae01018f2859b87d69a840b15fb5'}}, '901f04282f02771977b6f17bbfe1e42bb1577d9f': {'user': 'davidcarl', 'state': 'end', 'timestamp': '2018-09-25T08:06:00+0200', 'storage': {'issuehash': '2df195ddc6fd9153a2326ce55a718455ca5e79bc', 'linehash': '901f04282f02771977b6f17bbfe1e42bb1577d9f'}}, '2b660624249cd63db721810a7b5c5ff6216075a5': {'user': 'davidcarl', 'state': 'start', 'timestamp': '2018-09-25T08:06:00+0200', 'storage': {'issuehash': '2df195ddc6fd9153a2326ce55a718455ca5e79bc', 'linehash': '2b660624249cd63db721810a7b5c5ff6216075a5'}}, '5a00c3930a7e6321c3b77ca7e331c6d13d59b7b4': {'user': 'davidcarl', 'state': 'end', 'timestamp': '2018-09-25T08:06:00+0200', 'storage': {'issuehash': '2df195ddc6fd9153a2326ce55a718455ca5e79bc', 'linehash': '5a00c3930a7e6321c3b77ca7e331c6d13d59b7b4'}}, 'ea16293a47e783e1ea74c3ade5a63d204de95f31': {'user': 'davidcarl', 'state': 'start', 'timestamp': '2018-09-25T08:41:00+0200', 'storage': {'issuehash': '2df195ddc6fd9153a2326ce55a718455ca5e79bc', 'linehash': 'ea16293a47e783e1ea74c3ade5a63d204de95f31'}}, '6360c0de47e1c7bc456c8e213ba7584849a2684e': {'user': 'davidcarl', 'state': 'end', 'timestamp': '2018-09-25T08:41:00+0200', 'storage': {'issuehash': '2df195ddc6fd9153a2326ce55a718455ca5e79bc', 'linehash': '6360c0de47e1c7bc456c8e213ba7584849a2684e'}},
                                                                 '7ba6a3ac15c776f4848d3eb9b978b3c0dc4d1801': {'user': 'davidcarl', 'state': 'start', 'timestamp': '2018-09-25T08:44:00+0200', 'storage': {'issuehash': '2df195ddc6fd9153a2326ce55a718455ca5e79bc', 'linehash': '7ba6a3ac15c776f4848d3eb9b978b3c0dc4d1801'}}, '58056171fbd3cbefd8b161d78fd4fff9f010525d': {'user': 'davidcarl', 'state': 'end', 'timestamp': '2018-09-25T08:44:00+0200', 'storage': {'issuehash': '2df195ddc6fd9153a2326ce55a718455ca5e79bc', 'linehash': '58056171fbd3cbefd8b161d78fd4fff9f010525d'}}, 'a602878548affc03399c9a53a7ccf02faca737df': {'user': 'davidcarl', 'state': 'start', 'timestamp': '2018-09-25T08:44:00+0200', 'storage': {'issuehash': '2df195ddc6fd9153a2326ce55a718455ca5e79bc', 'linehash': 'a602878548affc03399c9a53a7ccf02faca737df'}}, '3543633e336ca7a6718d64969e9ff819105d2153': {'user': 'davidcarl', 'state': 'end', 'timestamp': '2018-09-25T08:46:00+0200', 'storage': {'issuehash': '2df195ddc6fd9153a2326ce55a718455ca5e79bc', 'linehash': '3543633e336ca7a6718d64969e9ff819105d2153'}}, 'b6af662f075c8e13a8730f02717a85b033c81305': {'user': 'davidcarl', 'state': 'start', 'timestamp': '2018-09-25T08:50:00+0200', 'storage': {'issuehash': '2df195ddc6fd9153a2326ce55a718455ca5e79bc', 'linehash': 'b6af662f075c8e13a8730f02717a85b033c81305'}}, '96b8f277195b658dab43b652f4264dde9bdc189f': {'user': 'davidcarl', 'state': 'end', 'timestamp': '2018-09-25T08:50:00+0200', 'storage': {'issuehash': '2df195ddc6fd9153a2326ce55a718455ca5e79bc', 'linehash': '96b8f277195b658dab43b652f4264dde9bdc189f'}}}}
        start_list, end_list = shared.listsplitter(testdata)
        self.assertEqual(start_list, [{'user': 'davidcarl', 'state': 'start', 'timestamp': '2018-09-25T08:06:00+0200', 'storage': {'issuehash': '2df195ddc6fd9153a2326ce55a718455ca5e79bc', 'linehash': 'ce31b3b3492cae01018f2859b87d69a840b15fb5'}}, {'user': 'davidcarl', 'state': 'start', 'timestamp': '2018-09-25T08:06:00+0200', 'storage': {'issuehash': '2df195ddc6fd9153a2326ce55a718455ca5e79bc', 'linehash': '2b660624249cd63db721810a7b5c5ff6216075a5'}}, {'user': 'davidcarl', 'state': 'start', 'timestamp': '2018-09-25T08:41:00+0200', 'storage': {'issuehash': '2df195ddc6fd9153a2326ce55a718455ca5e79bc', 'linehash': 'ea16293a47e783e1ea74c3ade5a63d204de95f31'}}, {
                         'user': 'davidcarl', 'state': 'start', 'timestamp': '2018-09-25T08:44:00+0200', 'storage': {'issuehash': '2df195ddc6fd9153a2326ce55a718455ca5e79bc', 'linehash': '7ba6a3ac15c776f4848d3eb9b978b3c0dc4d1801'}}, {'user': 'davidcarl', 'state': 'start', 'timestamp': '2018-09-25T08:44:00+0200', 'storage': {'issuehash': '2df195ddc6fd9153a2326ce55a718455ca5e79bc', 'linehash': 'a602878548affc03399c9a53a7ccf02faca737df'}}, {'user': 'davidcarl', 'state': 'start', 'timestamp': '2018-09-25T08:50:00+0200', 'storage': {'issuehash': '2df195ddc6fd9153a2326ce55a718455ca5e79bc', 'linehash': 'b6af662f075c8e13a8730f02717a85b033c81305'}}])
        self.assertEqual(end_list, [{'user': 'davidcarl', 'state': 'end', 'timestamp': '2018-09-25T08:06:00+0200', 'storage': {'issuehash': '2df195ddc6fd9153a2326ce55a718455ca5e79bc', 'linehash': '901f04282f02771977b6f17bbfe1e42bb1577d9f'}}, {'user': 'davidcarl', 'state': 'end', 'timestamp': '2018-09-25T08:06:00+0200', 'storage': {'issuehash': '2df195ddc6fd9153a2326ce55a718455ca5e79bc', 'linehash': '5a00c3930a7e6321c3b77ca7e331c6d13d59b7b4'}}, {'user': 'davidcarl', 'state': 'end', 'timestamp': '2018-09-25T08:41:00+0200', 'storage': {'issuehash': '2df195ddc6fd9153a2326ce55a718455ca5e79bc', 'linehash': '6360c0de47e1c7bc456c8e213ba7584849a2684e'}}, {
                         'user': 'davidcarl', 'state': 'end', 'timestamp': '2018-09-25T08:44:00+0200', 'storage': {'issuehash': '2df195ddc6fd9153a2326ce55a718455ca5e79bc', 'linehash': '58056171fbd3cbefd8b161d78fd4fff9f010525d'}}, {'user': 'davidcarl', 'state': 'end', 'timestamp': '2018-09-25T08:46:00+0200', 'storage': {'issuehash': '2df195ddc6fd9153a2326ce55a718455ca5e79bc', 'linehash': '3543633e336ca7a6718d64969e9ff819105d2153'}}, {'user': 'davidcarl', 'state': 'end', 'timestamp': '2018-09-25T08:50:00+0200', 'storage': {'issuehash': '2df195ddc6fd9153a2326ce55a718455ca5e79bc', 'linehash': '96b8f277195b658dab43b652f4264dde9bdc189f'}}])