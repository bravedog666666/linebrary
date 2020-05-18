import googlebookapi
#import mculibrary
import json
import jsonpath
import bs4 as bs # BeautifulSoup
from bs4 import BeautifulSoup
import urllib.request as req
import urllib
import string
import requests

api = googlebookapi.Api()
imageurl=""
def getResponse(url):
    url = urllib.parse.quote(url, safe=string.printable) 
    request = req.Request(
        url,
        headers={
            "user-agent":
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36"
        }) 
    with req.urlopen(request) as response:
        data = response.read().decode("utf-8")
    return data
def googlebooksearsh(isbn):
    sourceCode=api.list('isbn:'+isbn)
    source=json.dumps(sourceCode)
    codestr=json.loads(source)
    img=jsonpath.jsonpath(codestr,"$..items..imageLinks..smallThumbnail")
    if img:
        for im in img:
            imageurl=im
    #elif img: 
     #   imagelist="http://www.fice.kyu.edu.tw/faceapp/isbn2books.aspx?isbn="+isbn
      #  imageurl=imagelist[0]
    else: imageurl="https://media.taaze.tw/showLargeImageByIsbn.ashx?width=120&isbn="+isbn
    if not img: imageurl="https://uco-mcu.primo.exlibrisgroup.com/discovery/img/icon_book.png"
    #print(imageurl)
    return (imageurl)
#print(sourceCode)

