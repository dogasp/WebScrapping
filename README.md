# WebScrapping

## Objectif
l'objectif de ce projet est de pouvoir automatiser le recrutement des joueurs pour mon clan World Of Tanks

## Description des différents programmes
main.py: 
- utilise la librairie requests, beautifulsoup 4 et user agent
- correspond au fichier principal, c'est celui qui contient les fonctions qui seront réutilisé dans d'autres programmes.
- Quand on le lance, il va demander la date à partir de laquelle on veut regarder l'historique, une fois cela fait, le programme va, pour chaque clan du fichier ListeClan.txt regarder tous les joueurs qui ont quitté ce clan après la date entrée. Pour chaque joueur, si ses statistiques conviennent pour mon clan, il est enregistré dans le fichier result.csv qui est la sortie du programme.

DeepClan.py:
- Utilise la librairie Selenium, beautifulsoup 4 et les fonctions du main.py
- à l'exécution, il demande à l'utilisateur d'entrer le nom d'un clan à investiguer, on peut lui renseigner un clan ou une plage de clan du fichier ListeClan.txt sous la forme Clan1:Clan2. Le programme va ensuite ouvrir la page https://eu.wargaming.net/clans/wot/ et entrer le nom du clan dans la bare de recherche, il sélectionne le premier résultat et défile la page. Une fois arrivé en bas de la page, il va enregistrer la page et faire la liste de tous les joueurs qui ont quitté le clan depuis sa création. Cette liste sera envoyé vers main.py pour être analysé et obtennir un result.csv avec les potentielles recrues.
- enregistre tous les joueurs ayant quitté un clan dans un fichier playerchecked.txt pour ne pas analyser deux fois le même joueur.

Recheck.py:
- Utilise les fonctions de main.py
- prend en entrée des index de joueurs dans playerchecked.txt afin de réanalyser leurs statistiques (si jamais certains se sont améliorés ou ont décidé de rejouer au jeu après un temps d'inactivité)

## Lancer un programme

Simplement executer un des fichier avec python3 et les librairies installées


## problèmes possible
Liste non exhaustive des problèmes fréquents:
- fichier playerchecked.txt inexistant: il suffit de la créer
- DeepCLan.py ne trouve aucun résultat: la recherche de BS4 dépend beaucoup de la langue de récupération de la page