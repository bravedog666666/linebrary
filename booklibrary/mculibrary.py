import urllib.request as req
import urllib
import string
import json
import jsonpath
import googlebook

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

search_text = "小王子"
limit = "10"
url = "https://uco-mcu.primo.exlibrisgroup.com/primaws/rest/pub/pnxs?blendFacetsSeparately=false&disableCache=false&getMore=0&inst=886UCO_MCU&lang=zh-tw&limit=%s&newspapersActive=false&newspapersSearch=false&offset=0&pcAvailability=true&q=any,contains,%s&qExclude=&qInclude=&refEntryActive=false&rtaLinks=true&scope=MyInstitution&skipDelivery=Y&sort=rank&tab=LibraryCatalog&vid=886UCO_MCU:886MCU_INST" % (limit, search_text)
sourceCode = getResponse(url)
codestr=json.loads(sourceCode)
item_list=jsonpath.jsonpath(codestr,"$..docs")[0] #全部資訊

book_all_list = []
journal_all_list = []
for item in item_list:
    if(item.get("pnx").get("display").get("type"))==[ "book" ]:
        book_all_list.append(item)
    else:journal_all_list.append(item)

book_list = [[book["pnx"]["display"]["title"][0],book.get("pnx").get("sort").get("author"),
              book.get("pnx").get("addata").get("isbn"),book.get("pnx").get("addata").get("date"),book.get("pnx").get("addata").get("edition"),book.get("pnx").get("control").get("sourcerecordid")] for book in book_all_list]

journal_list = [[journal["pnx"]["display"]["title"][0],journal.get("pnx").get("sort").get("author"),
              journal.get("pnx").get("addata").get("issn"),journal.get("pnx").get("addata").get("date"),journal.get("pnx").get("control").get("sourcerecordid")] 
                for journal in journal_all_list]
#print ("圖書")
#for i in book_list:
 #   print (i)
#print ("\n期刊")
#for i in journal_list:
 #   print (i)

#print (book_list[1][2][1])
#print (book_list[1][2][1])

def book_url(bookid):
    url2="https://uco-mcu.primo.exlibrisgroup.com/discovery/fulldisplay?docid=alma"+bookid+"&context=L&vid=886UCO_MCU:886MCU_INST&lang=zh-tw&search_scope=MyInst_and_CI&adaptor=Local%20Search%20Engine&tab=Everything&query=any,contains,"+search_text+"&offset=0"
    url2 = urllib.parse.quote(url2, safe=string.printable)
    return url2

bookid=""
book_name=""
journal_name=""
author =""
isbn =""
date =""
issn =""
version=""
book_imgurl=""


print ("圖書：\n")
for booklist in book_list:
    book_name=booklist[0]
    author=""
    isbn=""
    date =""
    version=""
    if booklist[1]:
        for aut in booklist[1]:
            author+=aut+" "
    else:author="未知"
    if booklist[2]:
        book_imgurl=googlebook.googlebooksearsh(booklist[2][0])
        for isb in booklist[2]:
            isbn+=isb+"\n"
    else:
        isbn="未知"
        book_imgurl="https://uco-mcu.primo.exlibrisgroup.com/discovery/img/icon_book.png"
    if booklist[3]:
        for dat in booklist[3]:
            date+=dat
    else:date="未知"
    if booklist[4]:
        for vers in booklist[4]:
            version+=vers
    else:version="未知"
    for idd in booklist[5]:
        bookid=idd
                      
    print("書封："+book_imgurl+"\n書名："+book_name+"\n作者："+author+"\n出版日期："+date+"\n版本："+version+"\nISBN："+isbn+"連結：\n"+book_url(bookid)+"\n")


print ("期刊：\n")
for journallist in journal_list:
    book_imgurl="https://uco-mcu.primo.exlibrisgroup.com/discovery/img/icon_journal.png"
    journal_name=""
    author=""
    issn=""
    date =""
    for journal in journallist[0]:
            journal_name+=journal
    if journallist[1]:
        for aut in journallist[1]:
            author+=aut+" "
    else:author="未知"
    if journallist[2]:
        for iss in journallist[2]:
            issn+=iss+"\n"
    else:issn="未知"
    if journallist[3]:
        for dat in journallist[3]:
            date+=dat
    else:date="未知"
    for idd in journallist[4]:
        bookid=idd
    
    print("書封："+book_imgurl+"\n書名："+journal_name+"\n作者："+author+"\n出版日期："+date+"\nISSN："+issn+"\n連結：\n"+book_url(bookid)+"\n")
#print(journal_list[0][0])
#print(book_list[0])