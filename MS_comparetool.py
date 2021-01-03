from database import Db
from str1 import *


def get_blocks_of_file(fh):
    #Ezt át kellene írni, hogy dictionary-t adjon vissza, ahol a kulcs a blokk neve,
    #a hozzá tartozó érték, pedig a blokk tartalma listában
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
        if pos_start != -1 and line1.is_separate(pos_start, len(block_start_pattern)) is True:          #block started
            name = line[len(block_start_pattern):].split()[0]
            name = name.replace("[", "").replace("]", "").replace(" ", "").replace("\n", "")
            started_blocks.append(name)
            my_dict[name] = []
        if len(started_blocks):
            my_dict[started_blocks[-1]].append(line)
        if pos_end != -1 and line1.is_separate(pos_end, len(block_end_pattern)) is True:               #block ended
            if len(started_blocks):
                blocks.append(started_blocks.pop())
            else:
                raise BlockError("Block ended with no start!")

    if len(started_blocks):
        raise BlockError("Block has no end!")
    return my_dict

class BlockError(Exception):
    pass



def get_procedure_from_file(f, procname):
    """
    Az eljárás ugyanúgy működik mint a get_procedure_from_db eljárás,
    azonban nem adatbázisból hanem a kapott fájlból veszi ki a forrást
    és visszaadja listában.
    :param f:
    :param procname:
    :return list of rows:
    """
    list_procname = []
    dict_procnames = get_blocks_of_file(f)
    for key in dict_procnames:
        if key == procname:
            list_procname = dict_procnames[key].copy()
    return list_procname

def compare_procedures(proc_file, proc_db):
    """
    Az eljárás összehasonlítja a kapott két listát. Ha nincs különbség, akkor üres listát ad vissza.
    Különbség esetén két listaelemet ad vissza. Az első az első lista első eltérő sora,
    a második a második lista első eltérő sora.

    :param proc_file:
    :param proc_db:
    :return diff:
    """
    diff = []
    i = 0
    while True:
        if proc_file[i] != proc_db[i]:
            diff.append(proc_file[i])
            diff.append(proc_db[i])
            break
        else:
            i += 1
    return diff

if __name__ == '__main__':
    db = Db()
    f = open('testdata/stored_procs.sql', 'r')
    procname = 'dbo.uspGetBillOfMaterials'
    proc_file = get_procedure_from_file(f, procname)
    f.close()
    conn = db.connect_database()
    proc_db = db.get_procedure(procname)
    actual = compare_procedures(proc_file, proc_db)
    if actual:
        print('Különbség van az adatbázisban és a fájlban a ' + procname + ' eljárásban:')
        print('Fájl')
        print(actual[0])
        print('DB')
        print(actual[1])
