import requests
from bs4 import BeautifulSoup
import io
import pandas as pd
import difflib

# Lijst van NS-stations maken

url = 'https://nl.wikipedia.org/wiki/Lijst_van_spoorwegstations_in_Nederland'
r = requests.get(url)
soup = BeautifulSoup(r.text, 'html.parser')
tables = soup.find_all('table', class_ = 'wikitable')


dfs = pd.read_html(io.StringIO(str(tables)))

df = pd.concat(dfs)

list_names = list(df['Naam'])

dict_names_sorted = {}

for name in list_names:
    name_clean = (
        name.
        lower().
        replace('(alleen bij evenementen)', '').
        replace('(alleen als de veerboot gaat)', '').
        replace('(alleen als het spoorwegmuseum open is)', '').
        replace('-', '').
        replace('/', '').
        replace("'", '').
        replace(' ', '')
    )

    name_sorted = ''.join(sorted(name_clean))

    dict_names_sorted[name_sorted] = dict_names_sorted.get(name_sorted, [])

    dict_names_sorted[name_sorted].append(name)


def NS_anagram_solver(name, dict_names_sorted):
    name_clean = (
        name.
        lower().
        replace('-', '').
        replace('/', '').
        replace("'", '').
        replace(' ', '')
    )

    name_sorted = ''.join(sorted(name_clean))

    try:
        print('Match:', dict_names_sorted[name_sorted])
    except:
        matches = difflib.get_close_matches(name_sorted, dict_names_sorted.keys())
        if matches:
            print('Close match:', dict_names_sorted[matches[0]])
        else:
            print('No match found')