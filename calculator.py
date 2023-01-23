from datetime import datetime
from datetime import timedelta
import json
from prompter import from_dict_to_pd, prompt_stats


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


DATE_FORMAT = "%d/%m/%Y"


def read_json_file(filename: str) -> dict:
    with open(filename) as json_file:
        return json.load(json_file)


def check_birthdate(birthdate: str) -> None:
    pass


def check_life_duration(life_duration: str) -> None:
    pass


def calc_majorite_date(birthdate: str) -> datetime:
    birth = datetime.strptime(birthdate, DATE_FORMAT)
    majorite = birth.replace(year=birth.year + 18)
    return majorite


def get_interest_calc_days(majorite: datetime, years: int) -> list:
    interest_date_liste = []
    end_date = majorite.replace(year=majorite.year + years)
    current_date = majorite

    while current_date != end_date:
        if current_date.day == 1 or current_date.day == 16:
            interest_date_liste.append(current_date.strftime(DATE_FORMAT))
        current_date = current_date + timedelta(days=1)
    return interest_date_liste


def get_interest_from_date(interest: dict, date: datetime) -> float:
    interest_dates = [key for key in interest]

    if datetime.strptime(interest_dates[-1], DATE_FORMAT) < date:
        return interest[interest_dates[-1]]

    interest_dates.reverse()
    for i_date in interest_dates:
        if datetime.strptime(i_date, DATE_FORMAT) <= date:
            return interest[i_date]


def get_interest_rate_by_days(icd_list: list) -> dict:
    interest: dict = read_json_file("cours.json")
    rates = []
    for icd in icd_list:
        rates.append(
            get_interest_from_date(
                interest,
                datetime.strptime(icd, DATE_FORMAT)
            )
        )

    return dict(zip(icd_list, rates))


def get_plafond_by_date(date: str) -> float:
    return get_plafond_by_datetime(datetime.strptime(date, DATE_FORMAT))


def get_plafond_by_datetime(date: datetime) -> float:
    plafonds: dict = read_json_file("plafond.json")
    plafonds_dates = [key for key in plafonds]

    if datetime.strptime(plafonds_dates[-1], DATE_FORMAT) < date:
        return plafonds[plafonds_dates[-1]]

    plafonds_dates.reverse()

    for i_date in plafonds_dates:
        if datetime.strptime(i_date, DATE_FORMAT) <= date:
            return plafonds[i_date]


def apply_interest(money: float, interest: float) -> float:
    return money * ((interest / 100) / 24)


def get_growth_data(ird_dict: dict) -> dict:
    money: float = 0.0
    money_historic = []
    date_historic = []
    year_interest: float = 0.0

    for date, interest in ird_dict.items():
        if date[:5] == "01/01":
            money += year_interest
            year_interest = 0
            money_historic.append(money)
            date_historic.append(date)
        plafond = get_plafond_by_date(date)
        if money < plafond:
            money = plafond
        year_interest += apply_interest(money, interest)

    return dict(zip(date_historic, money_historic))


def main() -> int:
    birthdate = input(bcolors.OKCYAN +
                      "Indiquez votre date de naissance ? (jj/mm/aaaa) : "
                      + bcolors.ENDC)
    check_birthdate(birthdate)

    life_duration = input(bcolors.OKBLUE +
                          "Indiquez la période de vie ? (en années) : "
                          + bcolors.ENDC)
    check_life_duration(life_duration)

    # majorite_date = calc_majorite_date(birthdate)
    majorite_date = datetime.strptime(birthdate, DATE_FORMAT)

    icd_list = get_interest_calc_days(majorite_date, int(life_duration))

    ird_dict = get_interest_rate_by_days(icd_list)
    growth_data = get_growth_data(ird_dict)

    print(json.dumps(growth_data, indent=2))

    prompt_stats(from_dict_to_pd(growth_data))

    exit(0)


main()
