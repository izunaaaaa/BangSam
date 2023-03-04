import json
import os


tmp = str(os.getcwd()) + "/BangSam/houses/"
print(tmp)
with open(tmp + "dong.json", "r") as f:
    dong_list = json.load(f)

new_list = []
for dong in dong_list:
    new_data = {"model": "houses.House"}
    new_data["fields"] = {}
    new_data["fields"]["name"] = dong
    new_list.append(new_data)

print(new_list)

with open("dong.json", "w", encoding=UTF - 8) as t:
    json.dump(new_list, t, ensure_ascii=False, indent=2)
