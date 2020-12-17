
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

    list1 = []
    list2 = []
    file1_started_blocks = []
    file2_started_blocks = []
    while True:
        line1 = f1.readline()
        line2 = f2.readline()
#        get_blocks(line1, file1_started_blocks, list1)
#        get_blocks(line2, file2_started_blocks, list2)

        x = get_closed_block_name(line1, file1_started_blocks)
        if x:
            list1.append(x)
        x = get_closed_block_name(line2, file2_started_blocks)
        if x:
            list2.append(x)

        if not line1 and not line2:
            f1MinusF2 = [x for x in list1 if x not in list2]
            f2MinusF1 = [x for x in list2 if x not in list1]
            break;

    return [f1MinusF2, f2MinusF1]

def get_blocks(line, list_sblocks, list_to_add):
    x = line.split()
    if len(x) >= 3:
        if x[2] and x[0] == "block" and x[2] == "start":
            list_sblocks.append(x[1])
        if x[2] and x[0] == "block" and x[2] == "end":
            if list_sblocks[-1] == x[1]:
                list_sblocks.pop()
                list_to_add.append(x[1])
            else:
                print("wrong block encapsulation!")

def get_closed_block_name(line, list_sblocks):
#returns block name if the block reached its end
    x = line.split()
    if len(x) >= 3:
        if x[2] and x[0] == "block" and x[2] == "start":
            list_sblocks.append(x[1])
        if x[2] and x[0] == "block" and x[2] == "end":
            if list_sblocks[-1] == x[1]:
                list_sblocks.pop()
                return x[1]
            else:
                print("wrong block encapsulation!")
    return None
