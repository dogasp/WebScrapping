from main import *

def recheck(players):
    rest = [] if len(players) == 0 else CheckPlayer(players)

    while len(rest) > 0:
        print(rest)
        rest = CheckPlayer(rest, False)

if __name__ == "__main__":
    with open('playerChecked.txt', 'r', encoding='utf-8') as file:
        playerChecked = file.read().split("\n")

    no = input("entrer les index (a:b) : ").split(":")
    liste = playerChecked[int(no[0]):int(no[1])]
    recheck(liste)
    