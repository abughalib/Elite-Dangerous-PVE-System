from bs4 import BeautifulSoup
import urllib3
import pandas as pd
import re
import csv
import vars
import copy
from urllib import parse
from time import sleep

http = urllib3.PoolManager()

# Get System Data

args = vars.all_args.parse_args()

ref_system = args.ref
ref_system_distance = args.dist
source_per_target = 1

print('''
Command: python main.py --fed 2 --imp 1 --all 1 --ind 1 --ref "Sol" --res "haz" --dist 100
fed: Minimum number of federation faction on that system.
imp: Minimum number of imperial faction on that system.
all: Minimum number of alliance faction on that system.
ind: Minimum number of Imperial Faction on that system.
ref: Reference system i.e From where you are planning to look for the systems.
res: Resource Extraction site types.
    "any": "Any site i.e rings, CNB, low, reg, high, haz",
    "ring": "Ring Site",
    "CNB": "Compressed Nav Beacon",
    "low": "Resource Extraction Site [Low]",
    "reg": "Resource Extraction Site [Medium]",
    "high": "Resource Extraction Site [High]",
    "haz": "Resource Extraction Site [Hazardous]"
dist: Maximum distance from the Reference system.

Ctrl + C to exit anytime during execution.
''')

sleep(1)

sites = {
    "any": "Any site i.e rings, CNB, low, reg, high, haz",
    "ring": "Ring Site",
    "CNB": "Compressed Nav Beacon",
    "low": "Resource Extraction Site [Low]",
    "reg": "Resource Extraction Site [Medium]",
    "high": "Resource Extraction Site [High]",
    "haz": "Resource Extraction Site [Hazardous]"
}

print("Getting System List from edtools.cc for: ")
print(
    f'''
    Reference System: {ref_system}
    Distance From Reference System: {ref_system_distance}
    Type of Bounty Hunting Site: {sites[args.res]}
    Minimum No of Federation Faction: {args.fed}
    Minimum No of Imperial Faction: {args.imp}
    Minimum No of Alliance Faction: {args.all}
    Minimum No of Independent Faction: {args.ind}
    '''
)

sleep(1)

# If you're not happy with useragent you can change it.
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0',
}
resp = http.request("GET", f"https://edtools.cc/pve?s={parse.quote(ref_system)}&md={ref_system_distance}&sc=",
                    headers=headers)



page = resp.data.decode('utf-8')

soup = BeautifulSoup(page, features='lxml')
table = ""
row = ""

try:
    table = soup.find("table")
except:
    print("Unknown Error Check System Name")
    exit(0)

try:
    rows = table.find_all("tr")
except:
    print("No System Found")
    exit(0)

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

fed_factions = int(args.fed)
imp_factions = int(args.imp)
all_factions = int(args.all)
ind_factions = int(args.ind)

res_site = args.res

print("Applying Filter...")

filtered_result = copy.deepcopy(df.query(
    f'Fed >= {fed_factions} & Imp >= {imp_factions} & All >= {all_factions} & Ind >= {ind_factions}'
))

index_to_delete = []

if res_site != "any":
    for (x, result) in enumerate(zip(filtered_result.index, filtered_result["RES/rings"])):
        site = re.search(f"{res_site}", result[1])
        if site is None:
            index_to_delete.append(result[0])

filtered_result.drop(index=index_to_delete, inplace=True)

print("Writing Filtered_List.html")
filtered_result.to_html("Filtered_List.html")

# Check the system State.

print("Checking System Status from Inara.cz")

index_to_delete = []

for (index, system) in enumerate(zip(filtered_result.index, filtered_result["Source System"])):

    print(f'Checking for conflict in: "{system[1]} " ', end='')

    resp_inara = http.request("GET", f"https://inara.cz/starsystem/?search={parse.quote(system[1])}", headers=headers)
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
            print("Conflict Detected.", end='')
            break
        else:
            previous_influence = inf
    print("")

filtered_result.drop(index=index_to_delete, inplace=True)

filtered_result.to_html("Final_Result.html")
