import unittest, subprocess, logging, importlib
from python_lib.test import *

class Test_gitmytest(unittest.TestCase):

    def setUp(self):
        print(" In method", self._testMethodName)

    def test_runable(self):
        run = subprocess.run(
            ['python3', 'git-mytest.py', '-h'], stdout=subprocess.PIPE)
        self.assertEqual(run.returncode, 0)

if __name__ == '__main__':
    importlib.reload(logging)    
    logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.CRITICAL) # set to critical to hide intentional warnings and errors from test console
    unittest.main()