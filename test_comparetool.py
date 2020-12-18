import unittest
from MS_comparetool import *

class Test_test_comparetool(unittest.TestCase):
    def test_comparefiles_sameNumberOfRows(self):
        f1 = open('testdata/a.txt', 'r')
        f2 = open('testdata/b.txt', 'r')
        res = compareFiles(f1,f2)
        f1.close()
        f2.close()
        self.assertEqual(2, res)

    def test_comparefilesdifferentNumberOfRows(self):
        f1 = open('testdata/b.txt', 'r')
        f2 = open('testdata/c.txt', 'r')
        res = compareFiles(f1,f2)
        f1.close()
        f2.close()
        self.assertEqual(2, res)

    def test_compareBlockNamesInfiles(self):
        f1 = open('testdata/block_a.txt', 'r')
        f2 = open('testdata/block_b.txt', 'r')
        res = compareBlockNamesInfiles(f1,f2)
        f1.close()
        f2.close()
        self.assertEqual([['B'], ['C']], res)

    def test_get_blocknames_in_file(self):
        f1 = open('testdata/stopred_procs.sql', 'r')
        block_start_pattern = 'CREATE PROCEDURE'
        block_end_pattern = 'END;'
        res = getBlockNames(f1, block_start_pattern, block_end_pattern)
        f1.close()
        self.assertEqual(['dbo.uspGetBillOfMaterials', 'dbo.uspGetEmployeeManagers'], res)


if __name__ == '__main__':
    unittest.main()
