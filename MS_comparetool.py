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
    #Úgy látom, hogy ezt már nem használjuk.
    #De a neve alapján van értelme
    #Ezt át kellene írni, hogy dictionary-t adjon vissza, ahol a kulcs a blokk neve, 
    #a hozzá tartozó érték, pedig a blokk tartalma listában
    started_blocks = []
    retlist = []
    while True:
        line = fh.readline()
        x = line.split()
        if len(x) >= 3:
            if x[2] and x[0] == "block" and x[2] == "start":
                started_blocks.append(x[1])
            if x[2] and x[0] == "block" and x[2] == "end":
                if started_blocks[-1] == x[1]:
                    started_blocks.pop()
                    retlist.append(x[1])
                else:
                    print("wrong block encapsulation!")
        if not line:
            break
    return retlist

class BlockError(Exception):
    pass

def getBlockNames(fh, block_start_pattern, block_end_pattern):
    started_blocks = []
    blocks = []
    block_error = False
    for idx,line in enumerate(fh.readlines()):
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
    connectdata = f.readline();
    conn = pyodbc.connect(connectdata)
    return conn

def query_database(conn, sqlstmt):
    cursor = conn.cursor()
    cursor.execute(sqlstmt)
    return [x[0] for x in cursor]

def is_separate(text, i, length):
    a = text[i-1:1]
    if i > 0 and text[i-1:1].isalnum() == True:
        return False
    if len(text) > i + length and text[i+length].isalnum() == True:
        return False
    return True
    

