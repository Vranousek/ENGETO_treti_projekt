"""
projekt_3.py: třetí projekt do Engeto Online Python Akademie

author: Daniel Vrána
email: deny.vrana@seznam.cz
discord: vranousek
"""

import requests
from bs4 import BeautifulSoup
import csv
import sys
from urllib.parse import urljoin

class ElectionScraper:
    def __init__(self):
        self.base_url = "https://volby.cz/pls/ps2017nss/"
        self.headers = {"User-Agent": "Mozilla/5.0"}

    def get_soup(self, url):
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            response.encoding = response.apparent_encoding
            return BeautifulSoup(response.text, "html.parser")
        except requests.exceptions.RequestException:
            return None

    def get_municipalities(self, base_url):
        soup = self.get_soup(base_url)
        if not soup:
            return []

        municipalities = []
        for row in soup.select("table.table tr")[2:]:
            cells = row.find_all("td")
            if len(cells) >= 3:
                link = cells[2].find("a")
                if link:
                    municipalities.append({
                        "code": cells[0].text.strip(),
                        "name": cells[1].text.strip(),
                        "link": urljoin(base_url, link["href"])
                    })
        return municipalities

    def get_results(self, muni):
        url = muni["link"]
        print(f"STAHUJI DATA Z URL: {url}")  # Vypíše URL při stahování dat
        soup = self.get_soup(url)
        if not soup:
            return None

        table = soup.find("table", {"id": "ps311_t1"})
        cells = table.find_all("td") if table else []

        data = {
            "code": muni["code"],
            "location": muni["name"],
            "registered": cells[3].text.strip() if len(cells) > 3 else "0",
            "envelopes": cells[4].text.strip() if len(cells) > 4 else "0",
            "valid": cells[7].text.strip() if len(cells) > 7 else "0"
        }

        for row in soup.select("div.t2_470 table tr")[1:]:
            party_cells = row.find_all("td")
            if len(party_cells) >= 3:
                party = party_cells[1].text.strip()
                votes = party_cells[2].text.strip().replace("\xa0", "")
                if party and votes.isdigit():
                    data[party] = votes

        return data

    def scrape(self, base_url, output_file):
        print(f"STAHUJI DATA Z VYBRANÉHO URL: {base_url}")
        municipalities = self.get_municipalities(base_url)
        print(f"Nalezeno {len(municipalities)} obcí")

        results = []
        for i, muni in enumerate(municipalities, 1):
            data = self.get_results(muni)
            if data:
                results.append(data)
                print(f"Zpracována obec {i}/{len(municipalities)}: {muni['name']}")

        fieldnames = ["code", "location", "registered", "envelopes", "valid"]
        for row in results:
            fieldnames.extend([k for k in row.keys() if k not in fieldnames])

        with open(output_file, "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=";")
            writer.writeheader()
            writer.writerows(results)

        print(f"UKLÁDÁM DO SOUBORU: {output_file}")
        print(f"UKONČUJI: election_scraper.py")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Použití: python projekt_3.py <URL> <VÝSTUPNÍ_SOUBOR.csv>")
        sys.exit(1)

    scraper = ElectionScraper()
    scraper.scrape(sys.argv[1], "vysledky_louny.csv")
