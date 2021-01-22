import urllib.request
import urllib
import re
import os

class GeoSearch:
    def __init__(self):
        self.results = []

    def getAllResults(self, term):
        #gdsUrl = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=gds&'
        #queryUrl = gdsUrl + 'term=' + term
        #ret = urllib.request.urlopen(queryUrl)
        #filename = str(ret.read())
        #ptrn = r'<Id>(\d*)</Id>'
        #UIDs = re.findall(ptrn, filename)
        #eSumsUrl = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=gds&id='
        #sumPtrn = r'<Item Name=\"title\" Type=\"String\">(.*)</Item>\\n\\t<Item Name=\"sum'
        #for UID in UIDs:
        #    eSumUrl = eSumsUrl + UID
        #    ret = urllib.request.urlopen(eSumUrl)
        #    filename = str(ret.read())
        #    summ = ''.join(re.findall(sumPtrn, filename))
        #    print('['+ UID + '] ' + summ)
        os.chdir('/Models/geoResults')
        q1_lines = []
        with open('q2.txt') as q1_in:
            for line in q1_in:
                print(line)

        


