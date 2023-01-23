import requests
import json
from datetime import datetime

API_ROUTE = "https://www.insee.fr/fr/information/convertisseur-franc-euro/"

def getConversion(year: str, devise: str, money: str) -> float:
    if devise == "1": return float(money)
    if int(year) <= 1901: year = str(1901)

    obj = {
        "somme": money,
        "monnaieOrigine": devise,
        "anneeOrigine": year,
        "monnaieConversion": "1",
        "anneeConversion": "2022"
    }

    year = datetime.today().year


    response = requests.post(API_ROUTE, json=obj)
    js = response.json()

    return float(js["resultatFormate"].replace(u'\xa0', u'').replace(',', '.'))

def main():
    json_file = open('raw_plafond.json')
    raw_plafond_dict : dict = json.load(json_file)

    ret = {}
    devise = {
        "F": "3",
        "f": "2",
        "e": "1",
    }

    for date, money in raw_plafond_dict.items():
        value = getConversion(str(datetime.strptime(date, '%d/%m/%Y').year), devise[money[-1]], money[:-1])
        plafond_entry = {date: value}
        ret.update(plafond_entry)
    json_file.close()

    print(json.dumps(ret, indent=2))

main()