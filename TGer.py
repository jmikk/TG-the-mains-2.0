import requests
import time
from xml.dom.minidom import parseString
import os

# CONFIG
USER = input("User-Agent")


try:
    os.mkdir("TGS")
except FileExistsError:
    pass


def getItem(somthing):
    return somthing.firstChild.nodeValue


nat = input("What nation should I check the bids for?")
nat = nat.lower().replace(" ", "_")
response = requests.get(
    f"https://www.nationstates.net/cgi-bin/api.cgi?q=cards+asksbids;nationname={nat}",
    headers={"User-Agent": USER},
)
print("time.sleeping")
time.sleep(1)

document = parseString(str(response.text))
CARDIDs = document.getElementsByTagName("CARDID")
CARDSEASONS = document.getElementsByTagName("SEASON")
Name = document.getElementsByTagName("NAME")

count = 0
for each in CARDIDs:
    each = getItem(each)
    CS = getItem(CARDSEASONS[count])
    response2 = requests.get(
        f"https://www.nationstates.net/cgi-bin/api.cgi?q=card+owners;cardid={each};season={CS}",
        headers={"User-Agent": USER},
    )
    print("time.Sleeping part 2")
    time.sleep(1)
    document2 = parseString(str(response2.text))
    OWNERs = document2.getElementsByTagName("OWNER")
    listo = list()
    for everything in OWNERs:
        listo.append(getItem(everything))
        OWNERs = set(listo)
    total = list()
    request3 = requests.get("https://docs.google.com/spreadsheets/d/e/2PACX-1vS4k61P0kprfp3kULkwGzhSNdUvSkZokt-Ckm_FTJ-OWBQcwoAgCYKmiSdw0V1tLsAit5DZVdA9Nb8L/pub?gid=733627866&single=true&output=csv")
    pups = request3.text.split("\n")
    for main in OWNERs:
        for pup in pups:
            pup = pup.strip()
            # print(pup)
            puppet, mainer = pup.split(",")
            mainer = mainer.replace(" ", "_")
            mainer = mainer.lower()
            puppet = puppet.replace(" ", "_")
            puppet = puppet.lower()
            puppet = "|" + puppet + "|"
            main = "|" + main + "|"
            main = main.replace(puppet, mainer)
            main = main.replace("|", "")
        # print()
        total.append(main)
    OWNERs = set(total)

    print("Owners")
    print(OWNERs)
    for each3 in OWNERs:
        print("Adding " + str(each3))
        try:
            z = open("TGS/" + each3 + ".txt", "a")
            z.write(
                f"https://www.nationstates.net/page=deck/card={each}/season={getItem(CARDSEASONS[count])}/owners=1\n"
            )

        except FileNotFoundError:
            z = open("TGS/" + each3 + ".txt", "x")
            z.write(
                f"https://www.nationstates.net/page=deck/card={each}/season={getItem(CARDSEASONS[count])}/owners=1\n"
            )
    count = count + 1
