import pyodbc

def compareFiles(f1, f2):
    # A függvény összehasonlítja a két szövegfájl tartalmát.
    # Ha nincsen különbség 0-val tér vissza.
    # Különbség esetén az első különbséget tartalmazó sor számával tér vissza.
    # A fájlok első sora az 1-es sorszám.
    # Különbség esetén kiírja a következőt:
    # <első fájl neve>
    # első fájl eltérő sora
    # <második fájl neve>
    # második fájl eltérő sora
    cnt = 1
    while True:
        line1 = f1.readline()
        line2 = f2.readline()
        if not line1 or not line2:
            return 0
        if line1 != line2:
            return cnt
        cnt += 1

def compareBlockNamesInfiles(f1, f2):
    # A függvény blokkok neveit hasonlítja össze a fájlokban.
    # A blokk kezdetét a "block <blokknév> start" jelzi.
    # A blokk végét a "block <blokknév> end" jelzi.
    # Nem vizsgálja a blokkok tartalmát.
    # A függvény egy listát ad visssza, amely két listát tartalmaz.
    # Az első lista azokat a blokkneveket tartalmazza amelyek csak az első fájlban vannak meg,
    # a második azokat a blokkneveket amelyek csak a második fájlban vannak meg.
    # Ha a két fájl ugyanazokat a blokkneveket tartalmazza, akkor két üres listát ad vissza.

    list1 = get_blocks_of_file(f1)
    list2 = get_blocks_of_file(f2)
    f1MinusF2 = [x for x in list1 if x not in list2]
    f2MinusF1 = [x for x in list2 if x not in list1]
    return [f1MinusF2, f2MinusF1]


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
        if pos_start != -1 and is_separate(line, pos_start, len(block_start_pattern)) is True:          #block started
            name = line[len(block_start_pattern):].split()[0]
            name = name.replace("[", "").replace("]", "").replace(" ", "").replace("\n", "")
            started_blocks.append(name)
            my_dict[name] = []
        if len(started_blocks):
            my_dict[started_blocks[-1]].append(line)
        if pos_end != -1 and is_separate(line, pos_end, len(block_end_pattern)) is True:               #block ended
            if len(started_blocks):
                blocks.append(started_blocks.pop())
            else:
                raise BlockError("Block ended with no start!")

    if len(started_blocks):
        raise BlockError("Block has no end!")
    return my_dict

class BlockError(Exception):
    pass

def getBlockNames(fh, block_start_pattern, block_end_pattern):
    started_blocks = []
    blocks = []
    block_error = False
    for idx, line in enumerate(fh.readlines()):
        pos_start = line.lower().find(block_start_pattern.lower())
        pos_end = line.lower().find(block_end_pattern.lower())
        if pos_start != -1 and is_separate(line, pos_start, len(block_start_pattern)) == True:          #block started
            name = line[len(block_start_pattern):].split()[0]
            name = name.replace("[", "").replace("]", "").replace(" ", "").replace("\n", "")
            started_blocks.append(name)
        if pos_end != -1  and is_separate(line, pos_end, len(block_end_pattern)) == True:               #block ended
            if len(started_blocks):
                blocks.append(started_blocks.pop())
            else:
                raise BlockError("Block ended with no start!")
    if len(started_blocks):
        raise BlockError("Block has no end!")
    return blocks

def connect_database():
    f = open('.parameters', 'r', encoding='utf8')
    connectdata = f.readline()
    f.close()
    conn = pyodbc.connect(connectdata)
    return conn

def query_database(conn, sqlstmt):
    cursor = conn.cursor()
    cursor.execute(sqlstmt)
    return [x[0] for x in cursor]

def is_separate(text, i, length):
    if i > 0 and text[i-1:i-1+1].isspace() is False:
        return False
    if len(text) > i + length and text[i+length:i+length+1].isspace() is False:
        return False
    return True

def get_procedure_from_db(conn, procname):
    """
    A tárolt eljárás neve <séma.név> formátumban kell megadva legyen. pl : 'dbo.uspGetBillOfMaterials'
    Kérdezze le az adatbázisból a kapott tárolt eljárás szövegét és adja vissza listában!
    A szöveg elején és végén ne legyenek felesleges üres sorok.
    A lekérdezést beleírtam a get_procedure_from_db eljárásba.

    :param conn:
    :param procname:
    :return:
    """
    sqlstmt1 = "SELECT * FROM STRING_SPLIT(REPLACE(OBJECT_DEFINITION(object_id('"
    sqlstmt2 = "')), char(13) + Char(10), NCHAR(9999)), NCHAR(9999))"
    sqlstmt = sqlstmt1 + procname + sqlstmt2
    res = query_database(conn, sqlstmt)
    i = 0
    while len(res[i]) == 0:     #remove empty items from start
        res.pop(i)
    i = -1
    while len(res[i]) == 0:     #remove empty items from end
        res.pop(i)
    return res

def get_procedure_from_file(f, procname):
    """
    Az eljárás ugyanúgy működik mint a get_procedure_from_db eljárás,
    azonban nem adatbázisból hanem a kapott fájlból veszi ki a forrást
    és visszaadja listában.
    :param f:
    :param procname:
    :return list of rows:
    """
    dict_procnames = {}
    list_procname = []
    dict_procnames = get_blocks_of_file(f)
    for key in dict_procnames:
        if key == procname:
            list_procname = dict_procnames[key].copy()
            #list_procname = dict_procnames.items()
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
    print(is_separate("h el_ lo world", 2, 2))
