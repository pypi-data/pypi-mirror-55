import json
import os
import csv


class _Data:
    path = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(path, "data", "china_cities.csv")) as csv_file:
        reader = csv.reader(csv_file)
        next(reader)
        china_cities = [row[0].lower() for row in reader]
    with open(
        os.path.join(path, "data", "china_provinces.json"), encoding="utf-8"
    ) as json_file:
        china_provinces_dict = json.load(json_file)
        china_provinces = [
            row["Province"]
            .lower()
            .replace("province", "")
            .replace("region", "")
            .replace("municipality", "")
            .replace("special administrative", "")
            .replace("autonomous", "")
            .strip()
            for row in china_provinces_dict
        ]
