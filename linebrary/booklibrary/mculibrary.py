import urllib.request as req
import urllib
import string
import json
import jsonpath
from booklibrary.googlebook import googlebooksearsh

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

def book_url(search_text,bookid):
    url2="https://uco-mcu.primo.exlibrisgroup.com/discovery/fulldisplay?docid=alma"+bookid+"&context=L&vid=886UCO_MCU:886MCU_INST&lang=zh-tw&search_scope=MyInst_and_CI&adaptor=Local%20Search%20Engine&tab=Everything&query=any,contains,"+search_text+"&offset=0"
    url2 = urllib.parse.quote(url2, safe=string.printable)
    return url2

def getmculibrarylist(search_text):
    #search_text = "小王子"
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
    
    return book_list,journal_list


def getmculibrarybook(search_text,book_list):
    mcubooklibrary=[]

    bookid=""
    book_name=""
    author =""
    isbn =""
    date =""
    version=""
    book_imgurl=""

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
            book_imgurl=googlebooksearsh(booklist[2][0])
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
        book_imgurl_dict=dict([("圖片", book_imgurl)])
        book_name_dict=dict([("書名", book_name)])
        book_author_dict=dict([("作者", author)])
        book_date_dict=dict([("出版日期", date)])
        book_version_dict=dict([("版本", version)])
        book_isbn_dict=dict([("ISBN", isbn)])
        book_url_dict=dict([("網址", book_url(search_text,bookid))])
        book_imgurl_dict.update(book_name_dict)
        book_imgurl_dict.update(book_author_dict)
        book_imgurl_dict.update(book_date_dict)
        book_imgurl_dict.update(book_version_dict)
        book_imgurl_dict.update(book_isbn_dict)
        book_imgurl_dict.update(book_url_dict)
        mcubooklibrary.append(book_imgurl_dict)
        #print(mcubooklibrary)                 
    #print("書封："+book_imgurl+"\n書名："+book_name+"\n作者："+author+"\n出版日期："+date+"\n版本："+version+"\nISBN："+isbn+"連結：\n"+book_url(bookid)+"\n")
    return mcubooklibrary


def getmculibraryjournal(search_text,journal_list):
    mcujournallibrary=[]
    bookid=""
    journal_name=""
    author =""
    date =""
    issn =""
    version=""
    book_imgurl=""
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
        book_imgurl_dict=dict([("圖片", book_imgurl)])
        book_name_dict=dict([("書名", journal_name)])
        book_author_dict=dict([("作者", author)])
        book_date_dict=dict([("出版日期", date)])
        book_version_dict=dict([("版本", version)])
        book_isbn_dict=dict([("ISSN", issn)])
        book_url_dict=dict([("網址", book_url(search_text,bookid))])
        book_imgurl_dict.update(book_name_dict)
        book_imgurl_dict.update(book_author_dict)
        book_imgurl_dict.update(book_date_dict)
        book_imgurl_dict.update(book_version_dict)
        book_imgurl_dict.update(book_isbn_dict)
        book_imgurl_dict.update(book_url_dict)
        mcujournallibrary.append(book_imgurl_dict)
        #print("書封："+book_imgurl+"\n書名："+journal_name+"\n作者："+author+"\n出版日期："+date+"\nISSN："+issn+"\n連結：\n"+book_url(bookid)+"\n")
    