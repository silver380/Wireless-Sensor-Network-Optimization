import json

def read_config(file_path):
    data = {}
    with open(file_path) as f:
        data = json.load(f)
    return data

def read_map(file_path):
    city_map = []
    with open(file_path) as f:
        for line in f:
            city_map.append(list(map(int,line.split(','))))
    return city_map


