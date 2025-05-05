from random import randint


bound = int(input("Граница "))
kol = int(input("Количество "))


def generator():
    spis = []
    for i in range(kol):
        a = randint(1, bound)
        b = randint(1, bound)
        spis.append([a, b])
    return spis


def writer(spis):
    with open("edges.txt", "w") as file:
        file.write("")
    for i in range(len(spis)):
        line = str(spis[i][0]) + " " + str(spis[i][1]) + "\n"
        with open("edges.txt", "a") as file:
            file.write(line)


if __name__ == "__main__":
    spis = generator()
    writer(spis)
        

