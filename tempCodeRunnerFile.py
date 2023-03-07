with open("default_data.json", "w", encoding="UTF-8") as m:
    json.dump(default_data, m, ensure_ascii=False, indent=2)