from requests import Session
from bs4 import BeautifulSoup
import json

session = Session()
headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "en-US,en;q=0.9",
    "cache-control": "max-age=0",
    "cookie": "didomi_token=eyJ1c2VyX2lkIjoiMTdhYzA5ZmQtOThjZC02MmEwLWFkMWUtNjQ2OGRhYjkzNzk0IiwiY3JlYXRlZCI6IjIwMjEtMDctMTlUMjE6MTU6NDUuNzM5WiIsInVwZGF0ZWQiOiIyMDIxLTA3LTE5VDIxOjE1OjQ1LjczOVoiLCJ2ZXJzaW9uIjoyLCJwdXJwb3NlcyI6eyJlbmFibGVkIjpbImRldmljZV9jaGFyYWN0ZXJpc3RpY3MiLCJnZW9sb2NhdGlvbl9kYXRhIl19LCJ2ZW5kb3JzIjp7ImVuYWJsZWQiOlsiZ29vZ2xlIiwiYzpwaW50ZXJlc3QiLCJjOmhvdGphciIsImM6bmV3LXJlbGljIiwiYzpjb21tMTAwIiwiYzpib29raXRzaC1LYjhuYkFEaCIsImM6Y29tbTEwMHZpLXdkbU1tNEo2IiwiYzpib29raXRsYS1NYVJnZ21QTiIsImM6ZG90bWV0cmljLWk4YnFnWkNMIiwiYzpkb3RtZXRyaWMtZ2IyZmpLQ0oiLCJjOmRvdG1ldHJpYy1yakFoZXBSZyIsImM6aXNsb25saW5lLUY5R0JncFFoIiwiYzpldGFyZ2V0LVd3RWpBUTNHIiwiYzpzdHlyaWEtcWhVY2trWmUiLCJjOnhpdGktQjN3Ym5KS1IiLCJjOmdvb2dsZWFuYS0yM2RkY3JEaCJdfSwidmVuZG9yc19saSI6eyJlbmFibGVkIjpbImdvb2dsZSJdfSwiYWMiOiJBa3VBRUFGa0JKWUEuQWt1QUNBa3MifQ==; euconsent-v2=CPJmzMRPJmzMRAHABBENBjCsAP_AAH_AAAAAIEtf_X__b3_j-_59f_t0eY1P9_7_v-0zjhfdt-8N2f_X_L8X42M7vF36pq4KuR4Eu3LBIQdlHOHcTUmw6okVrzPsbk2Mr7NKJ7PEmnMbO2dYGH9_n93TuZKY7__8___z__-v_v____f_r-3_3__59X---_e_V399zLv9_____9nN__4ICAEmGpfQBdiWODJtGlUKIEYVhIdAKACigGFomsIGVwU7K4CPUELABCagIwIgQYgoxYBAAIBAEhEQEgB4IBEARAIAAQAqQEIACNgEFgBYGAQACgGhYgRQBCBIQZHBUcpgQESLRQT2VgCUXexphCGUWAFAo_oqMBEoQQLAyEhYOY4AkAAA.f_gAD_gAAAAA; njuskalo_adblock_detected=true; PHPSESSID=020d5f50a36b52b9f88308a3dbbe8c0a; __uzma=5d833c90-df15-485a-87dc-90cb9fbfa4a4; __uzmb=1626729339; comm100_visitorguid_1000306=dd93a53c-52a2-4bef-ad4e-cb529213982e; __uzmc=4212610090644; uzdbm_a=8a89a74b-851d-7c60-8235-4e1452fd7b65; __uzmd=1626736327",
    "dnt": "1",
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "none",
    "sec-fetch-user": "?1",
    "sec-gpc": "1",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

class njuskalo:
    def __init__(self):
        self.url = "https://www.njuskalo.hr/graficke-kartice"

    def load_url(self, url = None):
        """
        Just a inclass wrapper for load url
        """
        if not url:
            url = self.url

        resp = session.get(url, headers=headers)
        soup = BeautifulSoup(resp.text, features="lxml")
        return soup

    def is_blocked(self, soup)-> bool:
        title = soup.find("title")
        return True if title.string == "ShieldSquare Captcha" else False

    def load_listing(self, soup)-> list:
        """
        Extracts all gpus listings from soup
        List model:
            [
                {title, url, price, image_url, created_at},
                {title, url, price, image_url, created_at}
            ]
        """
        gpus = []
        elem = soup.find_all("ul", {"class": "EntityList-items"})
        if len(elem) == 3:
            elem = elem[1]
        else:
            elem = elem[0]

        for listing in elem.find_all("li"):
            if " ".join(listing.get("class")).startswith("EntityList-item EntityList-item--Regular"):
                title = listing.find("a", {"class": "link"}).contents[0].strip().lower()
                url = listing.find("a", {"class": "link"}).get("href")
                url = "https://www.njuskalo.hr" + url
                price = listing.find("strong").contents[0].strip()
                if "." in price:
                    price = float(price) * 1000

                price = int(price)
                image = listing.find("img").get("data-src").replace("200x150", "w920x690")
                image = "https:" + image
                posted_date = listing.find("time").contents[0].strip()[:10]
                gpus.append({"title": title, "url": url, "price": price, "image_url": image, "created_at": posted_date})

        return gpus

    def is_last(self, soup)-> bool:
        elem = soup.find("nav", {"class": "Pagination"})
        elem = str(elem)
        return False if "Sljedeća" in elem else True

    def load_gpus(self, search = None, locationID = None, min_price = None, max_price = None, save=False, testing=False, filter = True):
        base_url = f"{self.url}?" if not search else f"https://www.njuskalo.hr/index.php?ctl=search_ads&keywords={search.replace(' ', '+')}?"
        page_n = 1
        data = []

        if locationID:
            base_url = f"{base_url}geo%5BlocationIds%5D={locationID}&"

        if min_price:
            base_url = f"{base_url}price%5Bmin%5D={min_price}&"

        if max_price:
            base_url = f"{base_url}price%5Bmax%5D={max_price}&"

        if not (max_price and min_price and locationID):
            base_url = f"{base_url}&"

        while True:
            if page_n == 1:
                url = base_url
            else:
                url = f"{base_url}page={page_n}"

            soup = self.load_url(url)
            if self.is_blocked(soup):
                print("Njuskalo blocked requests")
                exit()

            listings = self.load_listing(soup)
            data = data + listings

            if self.is_last(soup):
                break
            else:
                page_n = page_n + 1

        if filter == True:
            return self.filter_gpus(data)
        elif filter == False:
            return data
        else:
            return data if search else self.filter_gpus(data)

    def filter_gpus(self, gpus_data_list):
        valid_gpus = ["1060", "1070", "1080", "2060", "2070", "2080", "3060", "3070", "3080", "3090", "1660", "570", "580", "470", "480", "A5000", "VII", "A4500", "6800", "6900", "A4000", "5700", "vega", "5600", "6600"]
        blacklist = ["neispravno"]

        sorted_data_set = []
        for gpu_set in gpus_data_list:
            is_valid = False
            for word in blacklist:
                if word in gpu_set["title"].lower():
                    is_valid = False
                    break

                is_valid = True

            if is_valid:
                for vgpu in valid_gpus:
                    if vgpu in gpu_set["title"]:
                        sorted_data_set.append(gpu_set)
                        break

        return sorted_data_set
