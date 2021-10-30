#!/usr/bin/python3
#coding:utf8
import requests
import bs4
import time
import datetime
import random
import csv
import os
import itertools as it
import concurrent.futures
from fake_useragent import UserAgent
from math import floor

with open('config.txt', 'r') as file:
    data = [int(a.split("=")[1]) for a in file.read().split("\n")]
    MIN_WN8 = data[0]
    MIN_30D_BATTLES = data[1]

clanToken = 'https://wot-life.com/eu/clan/'
playerToken = 'https://wot-life.com/eu/player/'
ValidPlayer = 0

MAX_THREADS = 40

clans = []
with open('ListeClan.txt') as file:
    clans = file.read().split("\n")

players = []
ua = UserAgent()

def findPlayers(page):
    global players
    response = requests.get(page, headers = {'User-Agent': ua.random}, timeout=5)

    time.sleep(random.randint(1, 3))

    soup = bs4.BeautifulSoup(response.text, 'html.parser')
    table = soup.find_all("tr")

    for j in table:
        sub = j.find_all("td")
        left = False
        for elt in sub:
            if elt.find_all("i", {'class':'fa fa-arrow-right'}):
                left = True
        if left:
            val = str(sub[3].find_all("script")[0]).split(')')[0][-16:-6]
            dateLeft = datetime.datetime.fromtimestamp(int(val))
            if dateLeft > LastDate:
                players.append(sub[1].find_all("a")[0].text)

def ProceedPlayer(url):
    global ValidPlayer
    
    response = requests.get(url, headers = {'User-Agent': ua.random}, timeout=5)

    time.sleep(random.randint(1, 3))

    soup = bs4.BeautifulSoup(response.text, 'html.parser')
    
    if soup.find("div", {'class':"alert alert-warning"}):
        return

    clan = soup.find("div", {'class': 'clan-since' })
    if clan != None:
        return
    
    data = [url, url.split("/")[-1], '', 'global_battles', 'global_victories', 'global_wn8', 'global_average_tier', '', '30d_battles', '30d_victories', '30d_wn8', '30d_average_tier']
    table = soup.find("table", {'class':'stats-table table-md'})
    row = table.find_all("tr")

    for info in row:
        try:
            title = info.find_all("th")[0].text
        except:
            pass

        if title == "Battles":
            tmp = info.find_all("td")
            if int(tmp[3].text) < MIN_30D_BATTLES:
                return
            data[3 ] = tmp[0].text
            data[8] = tmp[3].text
        elif title == "Victories":
            tmp = info.find_all("td")
            data[4] = tmp[1].text
            data[9] = tmp[7].text
        elif title == "WN8":
            tmp = info.find_all("td")
            if float(tmp[0].text.replace(',', '.')) < MIN_WN8:
                return
            data[5] = tmp[0].text
            data[10] = tmp[3].text
        elif title == "Ø Tier":
            tmp = info.find_all("td")
            data[6] = tmp[0].text
            data[11] = tmp[3].text
            
    ValidPlayer += 1
    return data


def CheckPlayer(players, begin = True):
    TimedOut = []
    pages = []

    for player in players:
        pages.append(playerToken + player)

    threads = min(MAX_THREADS, len(pages))

    csvPath = "result.csv"
    for file in os.listdir():
        if ".csv" in file:
            csvPath = file
    
    with open(csvPath, 'a', newline='') as csvfile:
        spamwriter =  csv.writer(csvfile, delimiter=';', dialect="excel-tab")
        if begin:
            spamwriter.writerow(['Url', 'Player Name', '', 'Global Battles', 'Global Victories', 'Global WN8', 'Global_Ø_Tier', '', '30D Battles', '30D Victories', '30D Wn8', '30D_Ø_Tier', 'date:' + datetime.datetime.now().strftime('%d/%m/%Y %H:%M')])

        with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
            futur_data = {executor.submit(ProceedPlayer, page): page for page in pages}

            for future in concurrent.futures.as_completed(futur_data):
                data_ = futur_data[future]
                valid = True
                try:
                    data_ = future.result()
                except:
                    print(data_)
                    TimedOut.append(data_.split("/")[-1])
                    valid = False

                if data_ != None and valid:
                        spamwriter.writerow(data_)
    
    print("Nombre de recrues potentielles: ", ValidPlayer)
    return TimedOut

if __name__ == "__main__":
    try:
        with open('result.csv', 'r', newline='') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=';', dialect="excel-tab")
            for row in spamreader:
                if len(row) == 13:
                    last = row[-1][5:]

        with open('result.csv', 'w'):
            pass
    except:
        last = ""
    entry = input('Date de dernière vérification (jj/mm/aaaa hh:mm)' + (last != "") * ", entrer d pour dernière" + ' : ')
    if entry == "d":
        entry = last
    LastDate = datetime.datetime.strptime(entry, '%d/%m/%Y %H:%M')

    start = time.time()

    pages = []

    for clan in clans:
        pages.append(clanToken + clan)

    pages = pages

    print("C'est parti pour ", len(pages), " clans")

    threads = min(MAX_THREADS, len(pages))
    with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
        executor.map(findPlayers, pages)

    print("Il y a ", len(players), " joueurs à check")

    rest = [] if len(players) == 0 else CheckPlayer(players)

    while len(rest) > 0:
        print(rest)
        rest = CheckPlayer(rest, False)

    DeltaTime = (time.time()- start)/60
    print("Temps pris: ", DeltaTime//1, "minutes", floor(DeltaTime%1 * 60 * 10)/10, "secondes")

    input("Appuyez sur une touche pour continuer...")
