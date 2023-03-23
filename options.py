import json
import os

with open("options.json", "r", encoding="UTF-8") as json_data:
    options = json.load(json_data)

option_list = []
for a in options:
    option_data = {"model": "houses.Option", "fields": {"name": a["option"]}}
    option_list.append(option_data)

with open("option_list.json", "w", encoding="utf-8") as m:
    json.dump(option_list, m, ensure_ascii=False, indent=2)
