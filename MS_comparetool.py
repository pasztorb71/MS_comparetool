from database import Db
from str1 import *
from procfile import *

def compare_two_list(proc_file, proc_db):
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
    pf = Procfile('testdata/stored_procs.sql')

    procname = 'dbo.uspGetBillOfMaterials'
    proc_file = pf.get_procedure(procname)
    proc_db = db.get_procedure(procname)
    actual = compare_two_list(proc_file, proc_db)
    if actual:
        print('Különbség van az adatbázisban és a fájlban a ' + procname + ' eljárásban:')
        print('Fájl')
        print(actual[0])
        print('DB')
        print(actual[1])
