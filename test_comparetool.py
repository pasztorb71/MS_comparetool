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
        block_end_pattern = 'end;'
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

    def test_get_blocks_of_file(self):
        #Írtam leírást a get_blocks_of_file eljáráshoz az elvárt működésről
        f = open('testdata/stored_procs.sql', 'r')
        res = get_blocks_of_file(f)
        f.close()
        expected = ['dbo.uspGetBillOfMaterials', 'dbo.uspGetEmployeeManagers', 'dbo.uspLogError']
        actual = [x for x in res]
        self.assertListEqual(expected, actual)
        expected = [36, 32, 55] 
        actual = list(map(len, res.values()))
        self.assertListEqual(expected, actual)

    def test_is_separate(self):
        #Ezt még ki kell dolgoznom.
        pass

    def test_get_procedure_from_db(self):
        #Csináld meg a már üresen létrehozott get_procedure_from_db eljárást,
        #ami paraméterként kap egy db connection-t és egy tárolt eljárás nevét.ű
        #A tárolt eljárás neve <séma.név> formátumban kell megadva legyen. pl : 'dbo.uspGetBillOfMaterials'
        #Kérdezze le az adatbázisból a kapott tárolt eljárás szövegét és adja vissza listában!
        #A szöveg elején és végén ne legyenek felesleges üres sorok.
        #A lekérdezést beleírtam a get_procedure_from_db eljárásba.
        conn = connect_database()
        proc_text = get_procedure_from_db(conn, 'dbo.uspGetBillOfMaterials')
        actual = len(proc_text)
        expected = 36
        self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()
