import json
import os

with open("option.json", "r", encoding="UTF-8") as json_data:
    houses = json.load(json_data)

option_list = []

for option in options:
    flag = True
