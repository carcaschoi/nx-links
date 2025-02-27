from bs4 import BeautifulSoup
import requests
import json

url = "https://darthsternie.net/switch-firmwares/"

class Firmwares():
    def __init__(self):
        print("Init module: ", self.__module__)
        out = {}
        path = "firmwares.json"
        links = self.fetch_dl_links(url)
        for i in range(len(links[0])):
            link = links[1][i].find("a")
            if link is not None:
                out[links[0][i]] = link.get("href")
        
        change = False
        try:
            with open(path, 'r') as read_file:
                old = json.load(read_file)
                if(json.dumps(old) != json.dumps(out)):
                    print(path + " changed")
                    change = True
        except FileNotFoundError:
            print("File doesn't exist")
            change = True

        if(change):
            with open(path, 'w') as write_file:
                json.dump(out, write_file, indent=4)
            print("Updated " + path)


    def getContent(self, tag):
        return tag.contents[0]

    def fetch_dl_links(self, url):
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")
        table = soup.find_all("tbody")
        titles = list(map(self.getContent, (table[0].find_all("td", {"class": "column-1"}))))
        links = table[0].find_all("td", {"class": "column-5"})
        china_titles = list(map(self.getContent, table[1].find_all("td", {"class": "column-1"})))
        for i in range(len(china_titles)):
            china_titles[i] = "[China Firmware] " + china_titles[i]
        china_links = table[1].find_all("td", {"class": "column-5"})
        return [titles + china_titles, links + china_links]

package = Firmwares()