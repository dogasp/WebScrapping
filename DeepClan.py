#coding:utf-8
from selenium import webdriver
from main import *

def getData(clan):
    driver = webdriver.Chrome(executable_path=r"/home/dogasp/Downloads/chromedriver") #path to chromeDriver
    driver.get("https://eu.wargaming.net/clans/wot/")
    time.sleep(1)

    #remove side panel
    button = driver.find_element_by_xpath('//*[@id="mCSB_1"]/div[1]/a')
    button.click()

    time.sleep(1)

    #find button for search bar
    button = driver.find_element_by_xpath('//*[@id="js-topmenu"]/div/div/div/div[2]/form/a[2]/i')
    button.click()

    time.sleep(1)

    #enter text in searchbar
    bar = driver.find_element_by_xpath('//*[@id="js-topmenu"]/div/div/div/div[2]/form/div/div/div[2]/input')
    bar.send_keys(clan)

    time.sleep(1)

    #click first link
    button = driver.find_element_by_xpath('//*[@id="js-topmenu"]/div/div/div/div[2]/form/div/div/div[2]/div/div[2]/div/ul/li/a')
    button.click()

    #scroll down the page
    time.sleep(1)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    while True:
        button = driver.find_elements_by_xpath('//*[@id="js-newsfeed-block"]/div/div[5]/a')

        try:
            button[0].click()
        except:
            break

        time.sleep(1)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    
    data = driver.page_source
    driver.close()
    return data

def ProcessClanPage(data):
    global playerChecked, name
    #processing the data
    soup = bs4.BeautifulSoup(data, 'html.parser')
    name = soup.find('span', {'class': 'clan_name js-longname'}) #find clan's full name
    if name == None:
        name = '[' + currentClan + ']' #message si le nom du clan est trop grand
    else:
        name = name.text
    print("Clan: ", name)
    days = soup.find_all('div', {'class': 'feed-aggregate'})

    for day in days:
        left = [a for a in day.find_all('div', {'class': 'feed-aggregate_item js-feed-aggregate-item'}) if 'left the' in a.text]
        if len(left) > 0:
            left = left[0].text
        else:
            continue
        if 'Players' in left:
            tmp = left.split('.')[1].split(', ')
        else:
            tmp = [left.split(' ')[2]]
        
        for elt in tmp:
            #pour chaque joueur qui a quitté, on regarde si il n'est pas déjà dans la liste, si il n'as pas effacé son compte et si il n'as pas déjà été check

            if elt not in players and 'anonym_' not in elt and (elt not in playerChecked or debug):
                players.append(elt)
                if not debug:
                    playerChecked.append(elt)
    
    if not debug:
        playerChecked.append("")

if __name__ == "__main__":
    debug = False
    with open('playerChecked.txt', 'r', encoding='utf-8') as file:
        playerChecked = file.read().split("\n")
    
    clan = input("Nom du clan : ")
    if " " in clan:
        clan = clan.split(" ")[0]
        debug = True
    if ":" in clan:
        fromClan, toClan = clan.split(":")
        begin = clans.index(fromClan)
        end = clans.index(toClan)
        clan = clans[begin:end+1]
    else:
        clan = [clan]
    start = time.time()
    
    for i in range(len(clan)):
        players = []
        currentClan = clan[i]
        data = getData(clan[i])
        ProcessClanPage(data)

        readMode = 'w' if i == 0 else 'a'

        with open('{}.csv'.format(" ".join(clan)), readMode, newline='') as csvfile:
            spamwriter =  csv.writer(csvfile, delimiter=';', dialect="excel-tab")
            spamwriter.writerow([name])        

        print("Nombre de joueurs à check: %d" % (len(players)))

        rest = [] if len(players) == 0 else CheckPlayer(players)

        while len(rest) > 0:
            print(rest)
            rest = CheckPlayer(rest, False)
    
    with open('playerChecked.txt', 'w', encoding='utf-8') as file:
            file.write('\n'.join(playerChecked))

    DeltaTime = (time.time()- start)/60
    print("Temps pris: ", DeltaTime//1, "minutes", floor(DeltaTime%1 * 60 * 10)/10, "secondes")
