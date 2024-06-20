import csv
import json
import os

def convert_value(value):
    if value == "null":
        return None
        
    if value is None:
        return value

    try:
        if '.' in value:
            return float(value)
        return int(value)
    except ValueError:
        pass

    if value.upper() in ['TRUE', 'FALSE']:
        return value.upper() == 'TRUE'

    return value

def csv_to_json(csv_file_path, json_file_path):
    file_name_key = "hogehoge"

    data = []
    with open(csv_file_path, mode='r', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            processed_row = {}
            for key, value in row.items():
                if key is None:
                    continue

                value = convert_value(value)

                if '/' in key:
                    keys = key.split('/')
                    current_level = processed_row
                    for part in keys[:-1]:
                        if part not in current_level:
                            current_level[part] = {}
                        current_level = current_level[part]
                    current_level[keys[-1]] = value
                else:
                    processed_row[key] = value
            data.append(processed_row)

    final_structure = {
        "user": "admin",
        "nakkohyo": data
    }

    with open(json_file_path, mode='w', encoding='utf-8') as json_file:
        json.dump(final_structure, json_file, ensure_ascii=False, indent=4)

csv_file_path = '/workspaces/hakke/sample/daneki/app/data/nakko/nakko_kajurin.csv'
json_file_path = '/workspaces/hakke/sample/daneki/app/data/nakko/nakko_kajurin.json'
csv_to_json(csv_file_path, json_file_path)
