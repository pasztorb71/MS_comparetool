import unittest
from MS_comparetool import *
from database import Db
from procfile import Procfile

db = Db()




class Test_test_comparetool(unittest.TestCase):

    def test_connect_database(self):
        conn = db.connect_database()
        self.assertIsNotNone(conn)

    def test_query_database(self):
        conn = db.conn
        self.assertIsNotNone(conn)
        res = db.query_database("SELECT SPECIFIC_SCHEMA + '.' + SPECIFIC_NAME FROM INFORMATION_SCHEMA.ROUTINES WHERE ROUTINE_TYPE = 'PROCEDURE'")
        self.assertListEqual(['dbo.uspGetBillOfMaterials', 'dbo.uspGetEmployeeManagers', 
                              'dbo.uspGetManagerEmployees', 'dbo.uspGetWhereUsedProductID', 
                              'dbo.uspLogError', 'dbo.uspPrintError', 'dbo.uspSearchCandidateResumes', 
                              'HumanResources.uspUpdateEmployeePersonalInfo', 'HumanResources.uspUpdateEmployeeHireInfo', 
                              'HumanResources.uspUpdateEmployeeLogin'], 
                             res)

    def test_get_blocks_of_file(self):
        #Írtam leírást a get_blocks_of_file eljáráshoz az elvárt működésről
        f = Procfile('testdata/stored_procs.sql')
        res = f.get_blocks(f)
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
        conn = db.connect_database()
        proc_text = db.get_procedure('dbo.uspGetBillOfMaterials')
        actual = len(proc_text)
        expected = 36
        self.assertEqual(expected, actual)

    def test_get_procedure_from_file(self):
        f = open('testdata/stored_procs.sql', 'r')
        proc_text = get_procedure_from_file(f, 'dbo.uspGetBillOfMaterials')
        f.close()
        actual = len(proc_text)
        expected = 36
        self.assertEqual(expected, actual)

    def test_compare_procedures(self):
        f = open('testdata/stored_procs.sql', 'r')
        proc_file = get_procedure_from_file(f, 'dbo.uspGetBillOfMaterials')
        f.close()
        conn = db.conn
        proc_db = db.get_procedure('dbo.uspGetBillOfMaterials')
        actual = compare_procedures(proc_file, proc_db)
        self.assertTrue(actual) #Vagyis az eredmény nem üres lista


if __name__ == '__main__':
    unittest.main()
