import csv

DB = {}


def load_cities(path):
    global DB

    with open(path) as f:
        reader = csv.reader(f)

        for row in reader:
            DB[f'{row[0].upper()}, {row[1]}'] = [float(n) for n in row[2:]]


def lookup_city(city):
    global DB

    if len(DB) == 0:
        raise Exception('City database is not loaded. Call load_db')

    return DB[city.upper()]
