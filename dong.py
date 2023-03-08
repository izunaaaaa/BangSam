import json
import os

with open("dong.json", "r", encoding="UTF-8") as json_data:
    houses = json.load(json_data)

gu_list = []
dong_list = []

for dong in houses:
    flag = True
    gu_data = {"model": "houses.Gu_list"}
    gu_data["fields"] = {"name": dong["gu"]}
    if gu_list:
        if dong["gu"] in [i["fields"]["name"] for i in gu_list]:
            flag = False

    gu_data["pk"] = len(gu_list) + 1

    if flag:
        gu_list.append(gu_data)

    dong_data = {"model": "houses.Dong_list"}
    pk = [i["pk"] for i in gu_list if i["fields"]["name"] == dong["gu"]][0]
    dong_data["fields"] = {"gu": pk, "name": dong["dong"]}
    if dong_data["fields"] in [i["fields"] for i in dong_list]:
        continue
    dong_data["pk"] = len(dong_list) + 1
    dong_list.append(dong_data)

with open("gu_list.json", "w", encoding="UTF-8") as m:
    json.dump(gu_list, m, ensure_ascii=False, indent=2)

with open("dong_list.json", "w", encoding="UTF-8") as m:
    json.dump(dong_list, m, ensure_ascii=False, indent=2)

default_data = gu_list + dong_list

with open("default_data.json", "w", encoding="UTF-8") as m:
    json.dump(default_data, m, ensure_ascii=False, indent=2)
