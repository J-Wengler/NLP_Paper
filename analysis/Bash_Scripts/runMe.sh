#!/bin/bash

#./getFastTextWiki.sh
#./getBioWordVecs.sh
python3 ./NLTKImport.py
#python3 getQuery1.py
#python3 getQuery2.py
#python3 getQuery3.py
#python3 getQuery4.py
#python3 getQuery5.py
#python3 cleanText.py 
#python3 allKeywordSciSpacy.py  
#python3 allKeywordBioWordVec.py  
#python3 allKeywordFastTextWiki.py
#python3 allKeywordSpacy.py
#python3 allKeywordFastTextSKIPGRAM.py     
python3 allKeywordFastTextCBOW.py
#python3 allKeywordSpacyCBOW.py
#python3 getResults.py
