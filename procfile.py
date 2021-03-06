from str1 import *

class BlockError(Exception):
    pass

class Procfile:
	def __init__(self, filename):
		with open('testdata/stored_procs.sql', 'r') as f:
			self.blocks = self.read_blocks_from_file(f)

	def read_blocks_from_file(self, fh):
		# Ezt át kellene írni, hogy dictionary-t adjon vissza, ahol a kulcs a blokk neve,
		# a hozzá tartozó érték, pedig a blokk tartalma listában
		block_start_pattern = 'CREATE PROCEDURE'
		block_end_pattern = 'end;'
		started_blocks = []
		blocks = []
		my_dict = {}
		block_error = False
		for idx, line in enumerate(fh.readlines()):
			pos_start = line.lower().find(block_start_pattern.lower())
			pos_end = line.lower().find(block_end_pattern.lower())
			line1 = str1(line)
			if pos_start != -1 and line1.is_separate(pos_start, len(block_start_pattern)) is True:  # block started
				name = line[len(block_start_pattern):].split()[0]
				name = name.replace("[", "").replace("]", "").replace(" ", "").replace("\n", "")
				started_blocks.append(name)
				my_dict[name] = []
			if len(started_blocks):
				my_dict[started_blocks[-1]].append(line)
			if pos_end != -1 and line1.is_separate(pos_end, len(block_end_pattern)) is True:  # block ended
				if len(started_blocks):
					blocks.append(started_blocks.pop())
				else:
					raise BlockError("Block ended with no start!")

		if len(started_blocks):
			raise BlockError("Block has no end!")
		return my_dict

	def get_procedure(self, procname):
		"""
		Az eljárás ugyanúgy működik mint a get_procedure_from_db eljárás,
		azonban nem adatbázisból hanem a kapott fájlból veszi ki a forrást
		és visszaadja listában.
		:param procname:
		:return list of rows:
		"""
		list_procname = []
		dict_procnames = self.blocks
		for key in dict_procnames:
			if key == procname:
				list_procname = dict_procnames[key].copy()
		return list_procname

	def get_blocks(self):
		return self.blocks
