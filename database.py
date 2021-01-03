import pyodbc

class Db:
	def __init__(self):
		self.conn = self.connect_database()

	def connect_database(self):
		f = open('.parameters', 'r', encoding='utf8')
		connectdata = f.readline()
		f.close()
		conn = pyodbc.connect(connectdata)
		return conn

	def query_database(self, sqlstmt):
		cursor = self.conn.cursor()
		cursor.execute(sqlstmt)
		return [x[0] for x in cursor]

	def get_procedure(self, procname):
		"""
		A tárolt eljárás neve <séma.név> formátumban kell megadva legyen. pl : 'dbo.uspGetBillOfMaterials'
		Kérdezze le az adatbázisból a kapott tárolt eljárás szövegét és adja vissza listában!
		A szöveg elején és végén ne legyenek felesleges üres sorok.
		A lekérdezést beleírtam a get_procedure_from_db eljárásba.

		:param procname:
		:return:
		"""
		sqlstmt1 = "SELECT * FROM STRING_SPLIT(REPLACE(OBJECT_DEFINITION(object_id('"
		sqlstmt2 = "')), char(13) + Char(10), NCHAR(9999)), NCHAR(9999))"
		sqlstmt = sqlstmt1 + procname + sqlstmt2
		res = self.query_database(sqlstmt)
		i = 0
		while len(res[i]) == 0:  # remove empty items from start
			res.pop(i)
		i = -1
		while len(res[i]) == 0:  # remove empty items from end
			res.pop(i)
		return res
