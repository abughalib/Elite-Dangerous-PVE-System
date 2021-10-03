from bs4 import BeautifulSoup
import urllib3
import pandas as pd
import numpy as np
import re
import csv

'''
http = urllib3.PoolManager()

# Get System Data

ref_system = "SOL"
ref_system_distance = 10
source_per_target = 1

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0',
}
resp = http.request("GET",
                    f"https://edtools.cc/pve?s={ref_system}&md={ref_system_distance}&sc=", headers=headers)

page = resp.data.decode('utf-8')

'''

page = open("PVE.html").read()

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

df.fillna(0, inplace=True)

fed_factions = 0
imp_factions = 0
all_factions = 0
ind_factions = 0

# Any: 0, Ring 1, CNB = 2, Low = 3, reg = 4, high = 5, haz = 6
res_site_level = 0

res_sites = {
    0: "any",
    1: "ring",
    2: "CNB",
    3: "low",
    4: "reg",
    5: "high",
    6: "haz"
}

filtered_result = df.query(
    f'Fed >= {fed_factions} & Imp >= {imp_factions} & All >= {all_factions} & Ind >= {ind_factions}'
)

index_to_delete = []

if res_site_level != 0:
    for (x, result) in enumerate(filtered_result["RES/rings"]):
        site = re.search(f"{res_sites[res_site_level]}", result)
        if site is None:
            index_to_delete.append(x)

filtered_result.drop(index=index_to_delete, inplace=True)

filtered_result.to_html("Filtered_list.html")
