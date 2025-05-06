"""
main.py: třetí projekt do Engeto Online Python Akademie
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
            response.encoding = 'windows-1250'
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
            if len(cells) >= 3 and cells[2].find("a"):
                municipalities.append({
                    "code": cells[0].text.strip(),
                    "name": cells[1].text.strip(),
                    "link": urljoin(self.base_url, cells[2].find("a")["href"])
                })
        return municipalities

    def process_page(self, url):
        soup = self.get_soup(url)
        if not soup:
            return None, None, None, {}

        table = soup.find("table", {"id": "ps311_t1"})
        if not table:
            return 0, 0, 0, {}

        cells = table.find_all("td")
        try:
            registered = int(cells[3].text.replace('\xa0', ''))
            envelopes = int(cells[4].text.replace('\xa0', ''))
            valid = int(cells[7].text.replace('\xa0', ''))
        except (IndexError, ValueError):
            return 0, 0, 0, {}

        parties = {}
        for row in soup.select("div.t2_470 table tr")[1:]:
            cols = row.find_all("td")
            if len(cols) >= 3:
                party = cols[1].text.strip()
                votes = cols[2].text.replace('\xa0', '')
                if party and votes.isdigit():
                    parties[party] = int(votes)

        return registered, envelopes, valid, parties

    def get_results(self, muni):
        main_url = muni["link"]
        soup = self.get_soup(main_url)
        if not soup:
            return None

        precincts = soup.find_all("td", {"class": "cislo"})
        if precincts:
            total_registered = 0
            total_envelopes = 0
            total_valid = 0
            total_parties = {}

            for precinct in precincts:
                link = precinct.find("a")
                if not link:
                    continue
                
                precinct_url = urljoin(self.base_url, link["href"])
                reg, env, val, parties = self.process_page(precinct_url)
                
                total_registered += reg
                total_envelopes += env
                total_valid += val
                
                for party, votes in parties.items():
                    total_parties[party] = total_parties.get(party, 0) + votes

            return {
                "code": muni["code"],
                "location": muni["name"],
                "registered": str(total_registered),
                "envelopes": str(total_envelopes),
                "valid": str(total_valid),
                **total_parties
            }
        else:
            reg, env, val, parties = self.process_page(main_url)
            return {
                "code": muni["code"],
                "location": muni["name"],
                "registered": str(reg),
                "envelopes": str(env),
                "valid": str(val),
                **parties
            }

    def scrape(self, base_url, output_file):
        print(f"STAHUJI DATA Z VYBRANÉHO URL: {base_url}")
        municipalities = self.get_municipalities(base_url)
        print(f"Nalezeno {len(municipalities)} obcí")

        results = []
        fieldnames = set()
        for i, muni in enumerate(municipalities, 1):
            print(f"Zpracovávám {i}/{len(municipalities)}: {muni['name']}")
            data = self.get_results(muni)
            if data:
                results.append(data)
                fieldnames.update(data.keys())

        columns = ["code", "location", "registered", "envelopes", "valid"]
        columns += sorted([col for col in fieldnames if col not in columns])

        with open(output_file, "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.DictWriter(f, fieldnames=columns, delimiter=";")
            writer.writeheader()
            writer.writerows(results)

        print(f"UKLÁDÁM DO SOUBORU: {output_file}")
        print("UKONČUJI: election_scraper.py")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Použití: python main.py <URL> <VÝSTUPNÍ_SOUBOR.csv>")
        sys.exit(1)

    scraper = ElectionScraper()
    scraper.scrape(sys.argv[1], sys.argv[2])
