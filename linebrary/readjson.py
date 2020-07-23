import json

def readJSON():
    with open('library.json', encoding='utf8') as f:
        myjson = json.load(f).get('library')
    myjson = [lib for lib in myjson if all([lib.get('經度'), lib.get('緯度')])]
    return myjson
#print(myjson.get('library')[0])