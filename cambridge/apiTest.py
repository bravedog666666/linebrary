from skPublish import API
import json
import jsonpath
import bs4 as bs # BeautifulSoup
import sys
#import datetime


api = API(baseUrl='https://dictionary.cambridge.org/api/v1', accessKey="VD9MGVPizFsaXOqojJQNG5acpTBa96QbvsikAJqx0eQie41TPYUwhCu5ixUcIOsS")
# api = API(baseUrl=sys.argv[1]+'/api/v1/', accessKey=sys.argv[2])

dictionaries = api.getDictionaries()
#print (dictionaries)
dictionaries = json.loads(api.getDictionaries())
#print (dictionaries)

dict = dictionaries[0]
#print (dict)
dictCode = dict["dictionaryCode"]

search_text="book"
print ("Best matching") #最佳匹配
bestMatch = json.loads(api.searchFirst("english-chinese-traditional",search_text, "html"))
#print(bestMatch)
html_json=jsonpath.jsonpath(bestMatch,"$..entryContent")[0] 
html = bs.BeautifulSoup(html_json, "html.parser")
#print(html)
english_def = html.select(".definition .def")
chinese_def = html.select(".definition .trans")
#print(category)

explanation = [[en.text,zh.text] for en,zh in zip(english_def,chinese_def)]
#print(explanation)

#with open("data.txt",mode="a",encoding="utf-8") as file:
    #file.writelines("/n"+search_text+"/")
   # for exp in explanation:
    #    for e in exp:
     #       file.write(e+"/")

#with open("data.txt",mode="r",encoding="utf-8") as file:
    #for x in file:
     #   print(x)

for exp in explanation:
    for e in exp:
        print(e)

# print ("Search")
# print ("Result list")
# results = json.loads(api.search(dictCode, "ca", 1, 1))
# print (results)
# print ("Spell checking")  #拼音檢查
# spellResults = json.loads(api.didYouMean(dictCode, "dorg", 3))
# print (spellResults)
# print ("Best matching") #最佳匹配
# bestMatch = json.loads(api.searchFirst("british", "ca", "html"))
# print(bestMatch)

# print ("Nearby Entries")  #附近連結
# nearbyEntries = json.loads(api.getNearbyEntries(dictCode, bestMatch["entryId"], 3))
# print(nearbyEntries)

#mean = json.loads(api.didYouMean(dictCode,"dog",1))
#print(mean)
# now = datetime.datetime.now()  
# today = now.strftime("%Y-%m-%d %H:%M:%S")
# day = json.loads(api.getWordOfTheDay(dictCode,today,"%Y-%m-%d %H:%M:%S"))
# print(day) #每日一句
