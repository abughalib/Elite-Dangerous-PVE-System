from bs4 import BeautifulSoup
import urllib3
import pandas as pd
import re
import csv

http = urllib3.PoolManager()

# Get System Data

ref_system = "Balmus"
ref_system_distance = 100
source_per_target = 1

print("Getting System List from edtools.cc")

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0',
}
resp = http.request("GET",
                    f"https://edtools.cc/pve?s={ref_system}&md={ref_system_distance}&sc=", headers=headers)

page = resp.data.decode('utf-8')

soup = BeautifulSoup(page, features='lxml')
table = soup.find("table")
rows = table.find_all("tr")

with open("system_list.csv", "wt+", newline="") as f:
    writer = csv.writer(f)
    for row in rows:
        csv_row = []
        for cell in row.findAll(["td", "th"]):
            csv_row.append(cell.get_text())
        writer.writerow(csv_row)

df = pd.read_csv("system_list.csv")

print(f"Total System Found: {len(df)}")

df.fillna(0, inplace=True)

fed_factions = 0
imp_factions = 0
all_factions = 0
ind_factions = 0

res_site = "haz"

print("Applying Filter...")

filtered_result = df.query(
    f'Fed >= {fed_factions} & Imp >= {imp_factions} & All >= {all_factions} & Ind >= {ind_factions}'
)

index_to_delete = []

if res_site != "any":
    for (x, result) in enumerate(filtered_result["RES/rings"]):
        site = re.search(f"{res_site}", result)
        if site is None:
            index_to_delete.append(x)

filtered_result.drop(index=index_to_delete, inplace=True)

print("Writing Filtered_List.html")
filtered_result.to_html("Filtered_List.html")

# Check the system State.

print("Checking System Status from Inara.cz")

index_to_delete = []

for (index, system) in enumerate(zip(filtered_result.index, filtered_result["Source System"])):

    print(f"Checking for conflict in: {system[1]}...", end='')

    system_name = '+'.join(map(str, system[1].split()))

    # Cross checking system state from Inara.cz.

    resp_inara = http.request("GET", f"https://inara.cz/starsystem/?search={system_name}", headers=headers)
    inara_page = resp_inara.data.decode('utf-8')

    bs = BeautifulSoup(inara_page, 'lxml')

    faction_list = bs.find('table')
    rows = faction_list.find_all("tr")

    previous_influence = 0.0

    for (i, row) in enumerate(rows):
        if i == 0:
            continue
        inf = float(row.find_all(['td', 'th'])[-1].text[:-1])

        if previous_influence == inf:
            index_to_delete.append(system[0])
            print("Conflict Detected...")
            break
        else:
            previous_influence = inf
    print("")

filtered_result.drop(index=index_to_delete, inplace=True)

filtered_result.to_html("Final_Result.html")