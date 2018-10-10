import os, unittest, pytz
from tzlocal import get_localzone
from datetime import datetime
from python_lib import shared, metadata


class Test_metadata(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        shared.set_working_dir(os.getcwd())
        try:
            os.rename(shared.get_gitpath()[
                      :-5] + '.time', shared.get_gitpath()[:-5] + '.time.save')
        except:
            pass

    @classmethod
    def tearDownClass(self):
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

    def test_time_format(self):
        format = shared.get_time_format()

        local_tz = get_localzone()
        tz = pytz.timezone(str(local_tz))
        now = datetime.utcnow()
        now = tz.localize(now)

        expected = now.replace(hour=int(10), minute=int(10), second=int(00))
        self.assertEqual(metadata.time(chour=10, cminute=10),
                         expected.strftime(format))

    def test_meta_data_cleaner_time(self):
        starts = [{'user': 'davidcarl', 'state': 'start', 'timestamp': '2018-09-25T08:06:00+0200', 'storage': {'issuehash': '2df195ddc6fd9153a2326ce55a718455ca5e79bc', 'linehash': 'ce31b3b3492cae01018f2859b87d69a840b15fb5'}}, {'user': 'davidcarl', 'state': 'start', 'timestamp': '2018-09-25T08:06:00+0200', 'storage': {'issuehash': '2df195ddc6fd9153a2326ce55a718455ca5e79bc', 'linehash': '2b660624249cd63db721810a7b5c5ff6216075a5'}}, {'user': 'davidcarl', 'state': 'start', 'timestamp': '2018-09-25T08:41:00+0200', 'storage': {'issuehash': '2df195ddc6fd9153a2326ce55a718455ca5e79bc', 'linehash': 'ea16293a47e783e1ea74c3ade5a63d204de95f31'}},
                  {'user': 'davidcarl', 'state': 'start', 'timestamp': '2018-09-25T08:44:00+0200', 'storage': {'issuehash': '2df195ddc6fd9153a2326ce55a718455ca5e79bc', 'linehash': '7ba6a3ac15c776f4848d3eb9b978b3c0dc4d1801'}}, {'user': 'davidcarl', 'state': 'start', 'timestamp': '2018-09-25T08:44:00+0200', 'storage': {'issuehash': '2df195ddc6fd9153a2326ce55a718455ca5e79bc', 'linehash': 'a602878548affc03399c9a53a7ccf02faca737df'}}, {'user': 'davidcarl', 'state': 'start', 'timestamp': '2018-09-25T08:50:00+0200', 'storage': {'issuehash': '2df195ddc6fd9153a2326ce55a718455ca5e79bc', 'linehash': 'b6af662f075c8e13a8730f02717a85b033c81305'}}]
        self.assertEqual(metadata.get_clean_time_meta_data(starts), ['2018-09-25T08:06:00+0200', '2018-09-25T08:06:00+0200',
                                                                     '2018-09-25T08:41:00+0200', '2018-09-25T08:44:00+0200', '2018-09-25T08:44:00+0200', '2018-09-25T08:50:00+0200'])

    def test_workcalculator(self):
        starts = [{'user': 'davidcarl', 'state': 'start', 'timestamp': '2018-09-25T08:06:00+0200', 'storage': {'issuehash': '2df195ddc6fd9153a2326ce55a718455ca5e79bc', 'linehash': 'ce31b3b3492cae01018f2859b87d69a840b15fb5'}}, {'user': 'davidcarl', 'state': 'start', 'timestamp': '2018-09-25T08:06:00+0200', 'storage': {'issuehash': '2df195ddc6fd9153a2326ce55a718455ca5e79bc', 'linehash': '2b660624249cd63db721810a7b5c5ff6216075a5'}}, {'user': 'davidcarl', 'state': 'start', 'timestamp': '2018-09-25T08:41:00+0200', 'storage': {'issuehash': '2df195ddc6fd9153a2326ce55a718455ca5e79bc', 'linehash': 'ea16293a47e783e1ea74c3ade5a63d204de95f31'}},
                  {'user': 'davidcarl', 'state': 'start', 'timestamp': '2018-09-25T08:44:00+0200', 'storage': {'issuehash': '2df195ddc6fd9153a2326ce55a718455ca5e79bc', 'linehash': '7ba6a3ac15c776f4848d3eb9b978b3c0dc4d1801'}}, {'user': 'davidcarl', 'state': 'start', 'timestamp': '2018-09-25T08:44:00+0200', 'storage': {'issuehash': '2df195ddc6fd9153a2326ce55a718455ca5e79bc', 'linehash': 'a602878548affc03399c9a53a7ccf02faca737df'}}, {'user': 'davidcarl', 'state': 'start', 'timestamp': '2018-09-25T08:50:00+0200', 'storage': {'issuehash': '2df195ddc6fd9153a2326ce55a718455ca5e79bc', 'linehash': 'b6af662f075c8e13a8730f02717a85b033c81305'}}]
        ended = [{'user': 'davidcarl', 'state': 'end', 'timestamp': '2018-09-25T08:06:00+0200', 'storage': {'issuehash': '2df195ddc6fd9153a2326ce55a718455ca5e79bc', 'linehash': '901f04282f02771977b6f17bbfe1e42bb1577d9f'}}, {'user': 'davidcarl', 'state': 'end', 'timestamp': '2018-09-25T08:06:00+0200', 'storage': {'issuehash': '2df195ddc6fd9153a2326ce55a718455ca5e79bc', 'linehash': '5a00c3930a7e6321c3b77ca7e331c6d13d59b7b4'}}, {'user': 'davidcarl', 'state': 'end', 'timestamp': '2018-09-25T08:41:00+0200', 'storage': {'issuehash': '2df195ddc6fd9153a2326ce55a718455ca5e79bc', 'linehash': '6360c0de47e1c7bc456c8e213ba7584849a2684e'}},
                 {'user': 'davidcarl', 'state': 'end', 'timestamp': '2018-09-25T08:44:00+0200', 'storage': {'issuehash': '2df195ddc6fd9153a2326ce55a718455ca5e79bc', 'linehash': '58056171fbd3cbefd8b161d78fd4fff9f010525d'}}, {'user': 'davidcarl', 'state': 'end', 'timestamp': '2018-09-25T08:46:00+0200', 'storage': {'issuehash': '2df195ddc6fd9153a2326ce55a718455ca5e79bc', 'linehash': '3543633e336ca7a6718d64969e9ff819105d2153'}}, {'user': 'davidcarl', 'state': 'end', 'timestamp': '2018-09-25T08:50:00+0200', 'storage': {'issuehash': '2df195ddc6fd9153a2326ce55a718455ca5e79bc', 'linehash': '96b8f277195b658dab43b652f4264dde9bdc189f'}}]
        self.assertEqual(metadata.calc_time_worked(starts, ended), 120)

    def test_workcalculator_uneven(self):
        starts = [{'user': 'davidcarl', 'state': 'start', 'timestamp': '2018-09-25T08:05:00+0200', 'storage': {'issuehash': '2df195ddc6fd9153a2326ce55a718455ca5e79bc', 'linehash': 'ce31b3b3492cae01018f2859b87d69a840b15fb5'}}, {'user': 'davidcarl', 'state': 'start', 'timestamp': '2018-09-25T08:0:00+0200', 'storage': {'issuehash': '2df195ddc6fd9153a2326ce55a718455ca5e79bc', 'linehash': '2b660624249cd63db721810a7b5c5ff6216075a5'}}, {'user': 'davidcarl', 'state': 'start', 'timestamp': '2018-09-25T08:41:00+0200', 'storage': {'issuehash': '2df195ddc6fd9153a2326ce55a718455ca5e79bc', 'linehash': 'ea16293a47e783e1ea74c3ade5a63d204de95f31'}},
                  {'user': 'davidcarl', 'state': 'start', 'timestamp': '2018-09-25T08:44:00+0200', 'storage': {'issuehash': '2df195ddc6fd9153a2326ce55a718455ca5e79bc', 'linehash': '7ba6a3ac15c776f4848d3eb9b978b3c0dc4d1801'}}, {'user': 'davidcarl', 'state': 'start', 'timestamp': '2018-09-25T08:44:00+0200', 'storage': {'issuehash': '2df195ddc6fd9153a2326ce55a718455ca5e79bc', 'linehash': 'a602878548affc03399c9a53a7ccf02faca737df'}}, {'user': 'davidcarl', 'state': 'start', 'timestamp': '2018-09-25T08:50:00+0200', 'storage': {'issuehash': '2df195ddc6fd9153a2326ce55a718455ca5e79bc', 'linehash': 'b6af662f075c8e13a8730f02717a85b033c81305'}}]
        ended = [{'user': 'davidcarl', 'state': 'end', 'timestamp': '2018-09-25T08:06:00+0200', 'storage': {'issuehash': '2df195ddc6fd9153a2326ce55a718455ca5e79bc', 'linehash': '901f04282f02771977b6f17bbfe1e42bb1577d9f'}}, {'user': 'davidcarl', 'state': 'end', 'timestamp': '2018-09-25T08:06:00+0200', 'storage': {'issuehash': '2df195ddc6fd9153a2326ce55a718455ca5e79bc', 'linehash': '5a00c3930a7e6321c3b77ca7e331c6d13d59b7b4'}}, {'user': 'davidcarl', 'state': 'end', 'timestamp': '2018-09-25T08:41:00+0200', 'storage': {'issuehash': '2df195ddc6fd9153a2326ce55a718455ca5e79bc', 'linehash': '6360c0de47e1c7bc456c8e213ba7584849a2684e'}},
                 {'user': 'davidcarl', 'state': 'end', 'timestamp': '2018-09-25T08:44:00+0200', 'storage': {'issuehash': '2df195ddc6fd9153a2326ce55a718455ca5e79bc', 'linehash': '58056171fbd3cbefd8b161d78fd4fff9f010525d'}}]
        self.assertEqual(metadata.calc_time_worked(starts, ended), 420)

    def test_get_date_string(self):
        data = [{'user': 'davidcarl', 'state': 'start', 'timestamp': '2018-09-25T08:06:00+0200', 'storage': {
            'issuehash': '2df195ddc6fd9153a2326ce55a718455ca5e79bc', 'linehash': 'ce31b3b3492cae01018f2859b87d69a840b15fb5'}}]
        self.assertEqual(metadata.get_date(data), ['2018-09-25'])

    def test_get_date_list(self):
        data = [{'user': 'davidcarl', 'state': 'start', 'timestamp': '2018-09-25T08:06:00+0200', 'storage': {'issuehash': '2df195ddc6fd9153a2326ce55a718455ca5e79bc', 'linehash': '2b660624249cd63db721810a7b5c5ff6216075a5'}},
                {'user': 'davidcarl', 'state': 'start', 'timestamp': '2018-09-25T08:41:00+0200', 'storage': {'issuehash': '2df195ddc6fd9153a2326ce55a718455ca5e79bc', 'linehash': 'ea16293a47e783e1ea74c3ade5a63d204de95f31'}}]
        res = ['2018-09-25', '2018-09-25']
        self.assertEqual(metadata.get_date(data), res)

    def test_order_days(self):
        data = {'2df195ddc6fd9153a2326ce55a718455ca5e79bc': {'ce31b3b3492cae01018f2859b87d69a840b15fb5': {'user': 'davidcarl', 'state': 'start', 'timestamp': '2018-09-25T08:06:00+0200'}, '901f04282f02771977b6f17bbfe1e42bb1577d9f': {'user': 'davidcarl', 'state': 'end', 'timestamp': '2018-09-25T08:06:00+0200'}, '2b660624249cd63db721810a7b5c5ff6216075a5': {'user': 'davidcarl', 'state': 'start', 'timestamp': '2018-09-25T08:06:00+0200'}, '5a00c3930a7e6321c3b77ca7e331c6d13d59b7b4': {'user': 'davidcarl', 'state': 'end', 'timestamp': '2018-09-25T08:06:00+0200'}, 'ea16293a47e783e1ea74c3ade5a63d204de95f31': {'user': 'davidcarl', 'state': 'start', 'timestamp': '2018-09-25T08:41:00+0200'}, '6360c0de47e1c7bc456c8e213ba7584849a2684e': {'user': 'davidcarl', 'state': 'end',                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        'timestamp': '2018-09-25T08:41:00+0200'}, '7ba6a3ac15c776f4848d3eb9b978b3c0dc4d1801': {'user': 'davidcarl', 'state': 'start', 'timestamp': '2018-09-25T08:44:00+0200'}, '58056171fbd3cbefd8b161d78fd4fff9f010525d': {'user': 'davidcarl', 'state': 'end', 'timestamp': '2018-09-25T08:44:00+0200'}, 'a602878548affc03399c9a53a7ccf02faca737df': {'user': 'davidcarl', 'state': 'start', 'timestamp': '2018-09-25T08:44:00+0200'}, '3543633e336ca7a6718d64969e9ff819105d2153': {'user': 'davidcarl', 'state': 'end', 'timestamp': '2018-09-25T08:46:00+0200'}, 'b6af662f075c8e13a8730f02717a85b033c81305': {'user': 'davidcarl', 'state': 'start', 'timestamp': '2018-09-25T08:50:00+0200'}, '96b8f277195b658dab43b652f4264dde9bdc189f': {'user': 'davidcarl', 'state': 'end', 'timestamp': '2018-09-25T08:50:00+0200'}}}
        res = [{'user': 'davidcarl', 'state': 'start', 'timestamp': '2018-09-25T08:06:00+0200', 'storage': {'issuehash': '2df195ddc6fd9153a2326ce55a718455ca5e79bc', 'linehash': 'ce31b3b3492cae01018f2859b87d69a840b15fb5'}}, {'user': 'davidcarl', 'state': 'end', 'timestamp': '2018-09-25T08:06:00+0200', 'storage': {'issuehash': '2df195ddc6fd9153a2326ce55a718455ca5e79bc', 'linehash': '901f04282f02771977b6f17bbfe1e42bb1577d9f'}}, {'user': 'davidcarl', 'state': 'start', 'timestamp': '2018-09-25T08:06:00+0200', 'storage': {'issuehash': '2df195ddc6fd9153a2326ce55a718455ca5e79bc', 'linehash': '2b660624249cd63db721810a7b5c5ff6216075a5'}}, {'user': 'davidcarl', 'state': 'end', 'timestamp': '2018-09-25T08:06:00+0200', 'storage': {'issuehash': '2df195ddc6fd9153a2326ce55a718455ca5e79bc', 'linehash': '5a00c3930a7e6321c3b77ca7e331c6d13d59b7b4'}}, {'user': 'davidcarl', 'state': 'start', 'timestamp': '2018-09-25T08:06:00+0200', 'storage': {'issuehash': '2df195ddc6fd9153a2326ce55a718455ca5e79bc', 'linehash': 'ce31b3b3492cae01018f2859b87d69a840b15fb5'}}, {'user': 'davidcarl', 'state': 'end', 'timestamp': '2018-09-25T08:06:00+0200', 'storage': {'issuehash': '2df195ddc6fd9153a2326ce55a718455ca5e79bc', 'linehash': '901f04282f02771977b6f17bbfe1e42bb1577d9f'}}, {'user': 'davidcarl', 'state': 'start', 'timestamp': '2018-09-25T08:06:00+0200', 'storage': {'issuehash': '2df195ddc6fd9153a2326ce55a718455ca5e79bc', 'linehash': '2b660624249cd63db721810a7b5c5ff6216075a5'}}, {'user': 'davidcarl', 'state': 'end', 'timestamp': '2018-09-25T08:06:00+0200', 'storage': {'issuehash': '2df195ddc6fd9153a2326ce55a718455ca5e79bc', 'linehash': '5a00c3930a7e6321c3b77ca7e331c6d13d59b7b4'}}, {'user': 'davidcarl', 'state': 'start', 'timestamp': '2018-09-25T08:06:00+0200', 'storage': {'issuehash': '2df195ddc6fd9153a2326ce55a718455ca5e79bc', 'linehash': 'ce31b3b3492cae01018f2859b87d69a840b15fb5'}}, {'user': 'davidcarl', 'state': 'end', 'timestamp': '2018-09-25T08:06:00+0200', 'storage': {'issuehash': '2df195ddc6fd9153a2326ce55a718455ca5e79bc', 'linehash': '901f04282f02771977b6f17bbfe1e42bb1577d9f'}}, {'user': 'davidcarl', 'state': 'start', 'timestamp': '2018-09-25T08:06:00+0200', 'storage': {'issuehash': '2df195ddc6fd9153a2326ce55a718455ca5e79bc', 'linehash': '2b660624249cd63db721810a7b5c5ff6216075a5'}}, {'user': 'davidcarl', 'state': 'end', 'timestamp': '2018-09-25T08:06:00+0200', 'storage': {'issuehash': '2df195ddc6fd9153a2326ce55a718455ca5e79bc', 'linehash': '5a00c3930a7e6321c3b77ca7e331c6d13d59b7b4'}}, {'user': 'davidcarl', 'state': 'start', 'timestamp': '2018-09-25T08:06:00+0200', 'storage': {'issuehash': '2df195ddc6fd9153a2326ce55a718455ca5e79bc', 'linehash': 'ce31b3b3492cae01018f2859b87d69a840b15fb5'}}, {'user': 'davidcarl', 'state': 'end', 'timestamp': '2018-09-25T08:06:00+0200', 'storage': {'issuehash': '2df195ddc6fd9153a2326ce55a718455ca5e79bc', 'linehash': '901f04282f02771977b6f17bbfe1e42bb1577d9f'}}, {'user': 'davidcarl', 'state': 'start', 'timestamp': '2018-09-25T08:06:00+0200', 'storage': {'issuehash': '2df195ddc6fd9153a2326ce55a718455ca5e79bc', 'linehash': '2b660624249cd63db721810a7b5c5ff6216075a5'}}, {'user': 'davidcarl', 'state': 'end', 'timestamp': '2018-09-25T08:06:00+0200', 'storage': {'issuehash': '2df195ddc6fd9153a2326ce55a718455ca5e79bc', 'linehash': '5a00c3930a7e6321c3b77ca7e331c6d13d59b7b4'}}, {'user': 'davidcarl', 'state': 'start', 'timestamp': '2018-09-25T08:41:00+0200', 'storage': {'issuehash': '2df195ddc6fd9153a2326ce55a718455ca5e79bc', 'linehash': 'ea16293a47e783e1ea74c3ade5a63d204de95f31'}}, {'user': 'davidcarl', 'state': 'end', 'timestamp': '2018-09-25T08:41:00+0200', 'storage': {'issuehash': '2df195ddc6fd9153a2326ce55a718455ca5e79bc', 'linehash': '6360c0de47e1c7bc456c8e213ba7584849a2684e'}}, {'user': 'davidcarl', 'state': 'start', 'timestamp': '2018-09-25T08:41:00+0200', 'storage': {'issuehash': '2df195ddc6fd9153a2326ce55a718455ca5e79bc', 'linehash': 'ea16293a47e783e1ea74c3ade5a63d204de95f31'}}, {'user': 'davidcarl', 'state': 'end', 'timestamp': '2018-09-25T08:41:00+0200', 'storage': {'issuehash': '2df195ddc6fd9153a2326ce55a718455ca5e79bc', 'linehash': '6360c0de47e1c7bc456c8e213ba7584849a2684e'}}, {'user': 'davidcarl', 'state': 'start', 'timestamp': '2018-09-25T08:44:00+0200', 'storage': {'issuehash': '2df195ddc6fd9153a2326ce55a718455ca5e79bc', 'linehash': '7ba6a3ac15c776f4848d3eb9b978b3c0dc4d1801'}}, {'user': 'davidcarl', 'state': 'end', 'timestamp': '2018-09-25T08:44:00+0200', 'storage': {'issuehash': '2df195ddc6fd9153a2326ce55a718455ca5e79bc', 'linehash': '58056171fbd3cbefd8b161d78fd4fff9f010525d'}}, {'user': 'davidcarl', 'state': 'start', 'timestamp': '2018-09-25T08:44:00+0200', 'storage': {'issuehash': '2df195ddc6fd9153a2326ce55a718455ca5e79bc', 'linehash': 'a602878548affc03399c9a53a7ccf02faca737df'}}, {'user': 'davidcarl', 'state': 'start', 'timestamp': '2018-09-25T08:44:00+0200', 'storage': {'issuehash': '2df195ddc6fd9153a2326ce55a718455ca5e79bc', 'linehash': '7ba6a3ac15c776f4848d3eb9b978b3c0dc4d1801'}}, {'user': 'davidcarl', 'state': 'end', 'timestamp': '2018-09-25T08:44:00+0200', 'storage': {'issuehash': '2df195ddc6fd9153a2326ce55a718455ca5e79bc', 'linehash': '58056171fbd3cbefd8b161d78fd4fff9f010525d'}}, {'user': 'davidcarl', 'state': 'start', 'timestamp': '2018-09-25T08:44:00+0200', 'storage': {'issuehash': '2df195ddc6fd9153a2326ce55a718455ca5e79bc', 'linehash': 'a602878548affc03399c9a53a7ccf02faca737df'}}, {'user': 'davidcarl', 'state': 'start', 'timestamp': '2018-09-25T08:44:00+0200', 'storage': {'issuehash': '2df195ddc6fd9153a2326ce55a718455ca5e79bc', 'linehash': '7ba6a3ac15c776f4848d3eb9b978b3c0dc4d1801'}}, {'user': 'davidcarl', 'state': 'end', 'timestamp': '2018-09-25T08:44:00+0200', 'storage': {'issuehash': '2df195ddc6fd9153a2326ce55a718455ca5e79bc', 'linehash': '58056171fbd3cbefd8b161d78fd4fff9f010525d'}}, {'user': 'davidcarl', 'state': 'start', 'timestamp': '2018-09-25T08:44:00+0200', 'storage': {'issuehash': '2df195ddc6fd9153a2326ce55a718455ca5e79bc', 'linehash': 'a602878548affc03399c9a53a7ccf02faca737df'}}, {'user': 'davidcarl', 'state': 'end', 'timestamp': '2018-09-25T08:46:00+0200', 'storage': {'issuehash': '2df195ddc6fd9153a2326ce55a718455ca5e79bc', 'linehash': '3543633e336ca7a6718d64969e9ff819105d2153'}}, {'user': 'davidcarl', 'state': 'start', 'timestamp': '2018-09-25T08:50:00+0200', 'storage': {'issuehash': '2df195ddc6fd9153a2326ce55a718455ca5e79bc', 'linehash': 'b6af662f075c8e13a8730f02717a85b033c81305'}}, {'user': 'davidcarl', 'state': 'end', 'timestamp': '2018-09-25T08:50:00+0200', 'storage': {'issuehash': '2df195ddc6fd9153a2326ce55a718455ca5e79bc', 'linehash': '96b8f277195b658dab43b652f4264dde9bdc189f'}}, {'user': 'davidcarl', 'state': 'start', 'timestamp': '2018-09-25T08:50:00+0200', 'storage': {'issuehash': '2df195ddc6fd9153a2326ce55a718455ca5e79bc', 'linehash': 'b6af662f075c8e13a8730f02717a85b033c81305'}}, {'user': 'davidcarl', 'state': 'end', 'timestamp': '2018-09-25T08:50:00+0200', 'storage': {'issuehash': '2df195ddc6fd9153a2326ce55a718455ca5e79bc', 'linehash': '96b8f277195b658dab43b652f4264dde9bdc189f'}}]
        self.assertEqual(metadata.order_days(data), res)

    def test_extract_time_string(self):
        data = [{'user': 'davidcarl', 'state': 'start', 'timestamp': '2018-09-25T08:06:00+0200', 'storage': {
            'issuehash': '2df195ddc6fd9153a2326ce55a718455ca5e79bc', 'linehash': '2b660624249cd63db721810a7b5c5ff6216075a5'}}]
        self.assertEqual(metadata.extract_time(data), ['08:06:00+0200'])

    def test_extract_time_list(self):
        data = [{'user': 'davidcarl', 'state': 'start', 'timestamp': '2018-09-25T08:06:00+0200', 'storage': {'issuehash': '2df195ddc6fd9153a2326ce55a718455ca5e79bc', 'linehash': '2b660624249cd63db721810a7b5c5ff6216075a5'}},
                {'user': 'davidcarl', 'state': 'end', 'timestamp': '2018-09-25T09:07:00+0200', 'storage': {'issuehash': '2df195ddc6fd9153a2326ce55a718455ca5e79bc', 'linehash': '2b660624249cd63db721810a7b5c5ff6216075a5'}}]
        res = ['08:06:00+0200', '09:07:00+0200']
        self.assertEqual(metadata.extract_time(data), res)

    def test_extract_timestamp_string(self):
        data = [{'user': 'davidcarl', 'state': 'start', 'timestamp': '2018-09-25T08:06:00+0200', 'storage': {
            'issuehash': '2df195ddc6fd9153a2326ce55a718455ca5e79bc', 'linehash': '2b660624249cd63db721810a7b5c5ff6216075a5'}}]
        self.assertEqual(metadata.extract_timestamp(
            data), ['2018-09-25T08:06:00+0200'])

    def test_seconds_to_timestamp(self):
        self.assertEqual(metadata.seconds_to_timestamp(10000), '2:46:40')

    def test_split_on_days(self):
        data = {'2df195ddc6fd9153a2326ce55a718455ca5e79bc': {'ce31b3b3492cae01018f2859b87d69a840b15fb5': {'user': 'davidcarl', 'state': 'start',
                                                                                                          'timestamp': '2018-09-25T08:06:00+0200', 'storage': {'issuehash': '2df195ddc6fd9153a2326ce55a718455ca5e79bc', 'linehash': 'ce31b3b3492cae01018f2859b87d69a840b15fb5'}}}}
        ans = metadata.split_on_days(data)
        self.assertEqual(metadata.split_on_days(data), ans)
