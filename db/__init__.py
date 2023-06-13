import json

def read_data()->list:
    with open("db/data.json") as f:
        data = json.load(f)
    return data

def add_data(data, del_data=False):
    if del_data:
        with open("db/data.json","w") as f:
            json.dump(data,f,indent=6,ensure_ascii=False)
    else:
        txt = read_data()
        txt.append(data)
        with open("db/data.json","w") as f:
            json.dump(txt,f,indent=6,ensure_ascii=False)

