import urllib.request as req
from urllib.parse import urlparse, parse_qs
import urllib
import string
# import bs4 as bs # BeautifulSoup

def getResponse(url):
    url = urllib.parse.quote(url, safe=string.printable) # 處理中文網址，可有可無
    request = req.Request( #建立Request，與對方伺服器互動的第一步
        url,
        headers={
            "user-agent":
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36"
        }) #headers裡的東西是平常瀏覧網站會傳送的東西，用以假裝我們是正常使用者
    with req.urlopen(request) as response:
        data = response.read().decode("utf-8")
    return data

def getCategory(County):
    Category=""
    book_name="小王子"
    ISBN="&search_input=978986189906&search_field=ISBN&"
    if County ==("桃園市" or "新竹市" or "新竹縣" or "苗栗縣" or "雲林縣" or "嘉義市" or "嘉義縣" or "臺東縣" or "花蓮縣" or "澎湖縣"):
        Category=1
    elif County ==("臺北市" or "高雄市"):
        Category=2
    elif County ==("新北市"):
        Category=3
    elif County ==("基隆市" or "臺中市" or "臺南市"):
        Category=4
    elif County ==("屏東市" or "公共"):
        Category=5
    elif County =="南投市":
        Category=6
    elif County ==("彰化縣"):
        Category=7
    elif County ==("金門縣"):
        Category=8
    elif County ==("連江縣"):
        Category=9
    return Category
    
# page="1"
# County="桃園市"
# Countyurl=""
# book_name="小王子"
# ISBN="&search_input=978986189906&search_field=ISBN&"
# page="1"
# County="桃園市"
# Countyurl=""
def getCountyurl(County):
    Countyurl=""
   # if County =="基隆縣":
   #     Countyurl="https://kllib.klccab.gov.tw/webpac/" #需重新寫 search.cfm
    #if County =="臺北市":
     #   Countyurl="http://webcat.tpml.edu.tw/webpac/" #a 抓的到 但沒有bookname
    #if County =="新北市":
     #   Countyurl="https://webpac.tphcc.gov.tw/webpac/" #需重新寫 search.cfm
    if County =="桃園市":
        Countyurl="https://hylib.typl.gov.tw/" 
    elif County =="新竹市":
        Countyurl="https://webpac.hcml.gov.tw/webpac/"
    elif County =="新竹縣":
        Countyurl="http://203.71.213.54/"
    elif County =="苗栗縣":
        Countyurl="https://webpac.miaoli.gov.tw/"
    elif County =="雲林縣":
        Countyurl="http://library.ylccb.gov.tw/"
    elif County =="嘉義市":
        Countyurl="http://library.cabcy.gov.tw/"
    elif County =="嘉義縣":
        Countyurl="https://library.cycab.gov.tw/"
   # elif County =="高雄市":                            #沒有bookname
   #     Countyurl="https://webpac.ksml.edu.tw/"
    elif County =="臺東縣":
        Countyurl="http://library.ccl.ttct.edu.tw/"
    elif County =="花蓮縣":
        Countyurl="http://app.hccc.gov.tw/"
    elif County =="澎湖縣":
        Countyurl="https://webpac.ilccb.gov.tw/"
    return Countyurl


# print(html)

def getPublicbook(html,County):
    book_name_list=html.select(".bookname")  #全部書的書名
    book_detail_list=[book.select("li") for book in html.select(".bookDetail ul")]
    #book_detail_list = ['\n'.join((info.text).replace("\n","") for info in book) for book in book_detail_list]
    book_img_list=html.select(".preload")
    book_url_list=html.select(".booklist a.bookname")
    #book_detail_list = '\n'.join(for tail.text in bdetail for bdetail in book_detail_list) 
    books=[]
    for book,book_name,book_img,book_url in zip(book_detail_list,book_name_list,book_img_list,book_url_list):
        query = urlparse(book_img.get("src1").replace("\n","")).query
        if(query):
            query_string = parse_qs(query)
            image_url = query_string.get('i')
            image_url=image_url[0]
        else:
            image_url=book_img.get("src1").replace("\n","")
        bookname=dict([('書名',book_name.text.replace("\n",""))])
        bookimg=dict([('圖片',image_url.replace('http://', 'https://'))])
        bookurl=dict([('網址',getCountyurl(County)+book_url.get('href').replace("\n",""))])
        book_dict = dict([(info.text.split('：')[0], (info.text.split('：')[1].replace(":",""))) for info in book])
        bookimg.update(bookname)
        bookimg.update(book_dict)
        bookimg.update(bookurl)
        books.append(bookimg)
    return(books)

# for book in book_detail_list:
#     book_dict = dict([(info.text.split('：')[0], (info.text.split('：')[1])) for info in book])
#     books.append(book_dict)