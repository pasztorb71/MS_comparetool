
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



def compareBlockNamesInfiles1(f1, f2):
  list1 = f1.readlines()
  blocks1 = get_blocks1(list1)
  list1 = f2.readlines()
  blocks2 = get_blocks1(list1)
  f1MinusF2 = list(set(blocks1) - set(blocks2))
  f2MinusF1 = list(set(blocks2) - set(blocks1))
  return [f1MinusF2, f2MinusF1]

def get_blocks1(list1):
   startedblocks = []
   endedblocks = []
   blocks = []
   for line in list1:
       if re.match('block .* start', line):
           startedblocks.append(line.split()[2])
       if re.match('block .* end', line):
           endedblocks.append(line.split()[2])
   for i in startedblocks:
       if i in endedblocks:
           blocks.append(i)
   return blocks