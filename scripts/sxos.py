from bs4 import BeautifulSoup
import requests
import json

url = "https://sx.xecuter.com/#prod-sxos"

class SXOS():
    def __init__(self):
        print("Init module: ", self.__module__)
        out = {}
        res = self.fetch_sxos_links(url)
        if (res is not None): 
            for i in range(len(res[0])):
                title = res[0][i]
                link = res[1][i]
                out[title] = link

        path = "sxos.json"
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


    def fetch_sxos_links(self, url):
        try:
            page = requests.get(url)
            page.raise_for_status()
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout, requests.exceptions.HTTPError):
            print("SXOS Down")
            return None

        soup = BeautifulSoup(page.content, "html.parser")
        section = soup.find("section", {"id": "download"}).find_all("a")
        #print(section[0])
        titles = [None] * 2
        links = [None] * 2
        for i in range(2):
            #https://sx.xecuter.com/download/SXOS_beta_v3.0.5.zip
            links[i] = "https://sx.xecuter.com/" + str(section[i].get("href"))[2:]
            titles[i] = str(section[i].contents[1]).replace("download ", "")
        return [titles, links]

package = SXOS()