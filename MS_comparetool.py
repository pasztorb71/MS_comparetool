
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

    f1MinusF2 = []
    f2MinusF1 = []

    return [f1MinusF2, f2MinusF1]