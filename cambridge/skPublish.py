from urllib.parse import (urlencode, quote)
import urllib3

# try:
#     from urllib import urlencode
# except ImportError:
#     from urllib.parse import urlencode

class API(object):

    def _getBaseUrl(self):  
        return self._baseUrl

    def _setBaseUrl (self, baseUrl):   
        if baseUrl and baseUrl[-1] != '/':
            self._baseUrl = baseUrl + '/'
        else:
            self._baseUrl = baseUrl

    baseUrl = property(_getBaseUrl, _setBaseUrl)

    def __init__(self, baseUrl, accessKey, userAgent = urllib3):
        self.baseUrl = baseUrl
        self.accessKey = accessKey
        self.userAgent = userAgent 
        self.http = userAgent.PoolManager()

    def _buildUrl(self, *pathParts, **queryParts):   
        uri = self._baseUrl
        uri += "/".join([quote(p) for p in pathParts])

        nonNullQueryParts = {}
        for paramName, paramValue in queryParts.items():
            if paramValue is not None:
                nonNullQueryParts[paramName] = paramValue
        if nonNullQueryParts:
            uri +=  "?%s" % urlencode(nonNullQueryParts)
        return uri

    def _open(self, url):
        response = self.http.request('GET',url, headers={'accessKey': self.accessKey})
        body = response.data
        return body

    def getDictionaries(self):      #取得辭典
        url = self._buildUrl('dictionaries')
        return self._open(url)

    def getDictionary(self, dictionaryCode):    
        url = self._buildUrl('dictionaries', dictionaryCode)
        return self._open(url)

    def getEntry (self, dictionaryCode, entryId, entryFormat=None):
        url = self._buildUrl('dictionaries',
                              dictionaryCode,
                              'entries',
                              entryId,
                              format=entryFormat)
        return self._open(url)

    def getEntryPronunciations (self, dictionaryCode, entryId, lang):    #發音
        url = self._buildUrl('dictionaries',
                              dictionaryCode,
                              'entries',
                              entryId,
                              'pronunciations',
                              lang=lang)
        return self._open(url)

    def getNearbyEntries (self, dictionaryCode, entryId, entryNumber=None):
        url = self._buildUrl('dictionaries',
                              dictionaryCode,
                              'entries',
                              entryId,
                              'nearbyentries',
                              entrynumber=entryNumber)
        return self._open(url)

    def getRelatedEntries (self, dictionaryCode, entryId):
        url = self._buildUrl('dictionaries',
                              dictionaryCode,
                              'entries',
                              entryId,
                              'relatedentries')
        return self._open(url)

    def getWordOfTheDay(self, dictionaryCode=None, day=None, entryFormat=None):  #每日一句
        params = dict(day=day, format=entryFormat)
        url = None
        if dictionaryCode is not None:
            url = self._buildUrl('dictionaries',
                                  dictionaryCode,
                                  'wordoftheday',
                                  **params)
        else:
            url = self._buildUrl('wordoftheday',
                                 **params)
        return self._open(url)

    def getWordOfTheDayPreview(self, dictionaryCode=None, day=None):  #前一天每日一句
        params = dict(day=day)
        url = None
        if dictionaryCode is not None:
            url = self._buildUrl('dictionaries',
                                  dictionaryCode,
                                  'wordoftheday',
                                  'preview',
                                  **params)
        else:
            url = self._buildUrl('wordoftheday',
                                  'preview',
                                  **params)
        return self._open(url)

    def search(self, dictionaryCode, searchWord, pageSize=None, pageIndex=None) :
        url = self._buildUrl('dictionaries',
                              dictionaryCode,
                              'search',
                              q=searchWord,
                              pagesize=pageSize,
                              pageindex=pageIndex)
        return self._open(url)

    def searchFirst (self, dictionaryCode, searchWord, entryFormat=None): #最佳匹配 #單辭相關全部
        url = self._buildUrl('dictionaries',
                              dictionaryCode,
                              'search',
                              'first',
                              q=searchWord,
                              format=entryFormat)
        return self._open(url)

    def didYouMean(self, dictionaryCode, searchWord, entryNumber=None):  #拼音檢查
        url = self._buildUrl('dictionaries',
                              dictionaryCode,
                              'search',
                              'didyoumean',
                              q=searchWord,
                              entrynumber=entryNumber)
        return self._open(url)

    def getThesaurusList(self, dictionaryCode):   #辭庫列表
        url = self._buildUrl('dictionaries',
                              dictionaryCode,
                              'topics')
        return self._open(url)

    def getTopic (self, dictionaryCode, thesName, topicId):
        url = self._buildUrl('dictionaries',
                              dictionaryCode,
                              'topics',
                              thesName,
                              topicId)
        return self._open(url)
