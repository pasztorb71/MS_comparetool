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

    def test_comparefiles_differentNumberOfRows(self):
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
        f1 = open('testdata/stored_procs.sql', 'r')
        block_start_pattern = 'CREATE PROCEDURE'
        block_end_pattern = 'end;'
        res = getBlockNames(f1, block_start_pattern, block_end_pattern)
        f1.close()
        self.assertEqual(['dbo.uspGetBillOfMaterials', 'dbo.uspGetEmployeeManagers', 'dbo.uspLogError'], res)

    def test_getBlockNames_exception(self):
        f1 = open('testdata/stored_procs_exc.sql', 'r')
        block_start_pattern = 'CREATE PROCEDURE'
        block_end_pattern = 'GO'
        try :
            res = getBlockNames(f1, block_start_pattern, block_end_pattern)
            self.assertTrue(1==0)
        except BlockError:
            self.assertTrue(1==1)
        f1.close()

    def test_connect_database(self):
        conn = connect_database()
        self.assertIsNotNone(conn)

    def test_query_database(self):
        conn = connect_database()
        self.assertIsNotNone(conn)
        res=query_database(conn, "SELECT SPECIFIC_SCHEMA + '.' + SPECIFIC_NAME FROM INFORMATION_SCHEMA.ROUTINES WHERE ROUTINE_TYPE = 'PROCEDURE'")
        self.assertListEqual(['dbo.uspGetBillOfMaterials', 'dbo.uspGetEmployeeManagers', 
                              'dbo.uspGetManagerEmployees', 'dbo.uspGetWhereUsedProductID', 
                              'dbo.uspLogError', 'dbo.uspPrintError', 'dbo.uspSearchCandidateResumes', 
                              'HumanResources.uspUpdateEmployeePersonalInfo', 'HumanResources.uspUpdateEmployeeHireInfo', 
                              'HumanResources.uspUpdateEmployeeLogin'], 
                             res)
if __name__ == '__main__':
    unittest.main()
