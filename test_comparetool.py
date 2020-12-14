import unittest
from MS_comparetool import *

class Test_test_comparetool(unittest.TestCase):
    def test_comparefiles(self):
        f1 = open('a.txt', 'r')
        f2 = open('b.txt', 'r')
        res = compareFiles(f1,f2)
        f1.close()
        f2.close()
        self.assertEqual(2, res)

if __name__ == '__main__':
    unittest.main()
