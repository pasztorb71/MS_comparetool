from database import Db
from str1 import *

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
    dict_procnames = get_blocks(f)
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
