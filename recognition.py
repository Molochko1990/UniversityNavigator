def extract_route(s):
    s = s.upper().split()
    Blocks = ['И-', 'Э-', 'Р-', "ГУК-", "Т-", "ВХО","ВЫХОД"]
    Result = []
    for symbol in Blocks:
        for i in s:
            if i.count(symbol) == 1:
                i = i.replace('А', "1")
                i = i.replace('Б', "2")
                if i.count("ВХО") == 1:
                    Result.append("Р-0000")
                elif i.count("ВЫХОД") == 1:
                    Result.append("Р-0000")
                else:
                    Result.append(i)

    print(Result)
    return Result


def fixer(i):

    i = i.upper()
    i = i.replace('А', "1")
    i = i.replace('Б', "2")
    i = i.replace('ВХОД', "Р-0000")
    i = i.replace('ВЫХОД', "Р-0000")
    print(i)
    return i
