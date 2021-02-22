#!/bin/bash

#./getFastTextWiki.sh
#./getBioWordVecs.sh

#rm -f /Data/allQueries.txt

#python3 prepareQueryData.py "GSE27980 ,GSE12237,GSE12276,GSE99394,GSE66495,GSE34970,GSE111489,GSE44660,GSE52604,GSE129945,GSE129946,GSE38057,GSE66463,GSE52050,GSE14108,GSE18544,GSE76714,GSE43837,GSE73285,GSE60464,GSE57492,GSE28049,GSE17019,GSE20016,GSE26338,GSE46928,GSE161116,GSE69042,GSE134026,GSE125989,GSE44354,GSE23019,GSE28313,GSE74968,GSE79534,GSE117453,GSE138682,GSE70576,GSE126037,GSE126036,GSE98298,GSE50493,GSE114627,GSE116531,GSE38283,GSE24100,GSE23655,GSE67088,GSE51395,GSE51411,GSE43278,GSE86501,GSE103935" q1
#python3 prepareQueryData.py "GSE17400,GSE17400,GSE47962,GSE47960,GSE19137,GSE47961,GSE5972,GSE49262,GSE49263,GSE50000,GSE30589,GSE44274,GSE50855,GSE156544,GSE45042,GSE50101,GSE18574,GSE47963,GSE33266,GSE36016,GSE50878,GSE51386,GSE51387,GSE93283,GSE156759,GSE1739,GSE56677,GSE40824,GSE40827,GSE40840,GSE59185,GSE68820,GSE160163,GSE10820,GSE11042,GSE17892,GSE21802,GSE22991,GSE44956,GSE44960,GSE50223,GSE70611,GSE70613,GSE70614,GSE70616,GSE70615,GSE36969,GSE64660,GSE103686,GSE106977,GSE125170,GSE154589" q2
#python3 prepareQueryData.py "GSE42639,GSE42638,GSE41088,GSE43764,GSE48890,GSE36328,GSE60572,GSE60573" q3
#python3 prepareQueryData.py "GSE60673,GSE54499,GSE54498,GSE3721,GSE3722,GSE3725,GSE4416,GSE75401,GSE35038,GSE70536" q4
#python3 prepareQueryData.py "GSE47860,GSE47861,GSE72795,GSE27175,GSE19829,GSE155478,GSE55399,GSE60995,GSE60994,GSE149940,GSE73923,GSE121682,GSE69428,GSE69429,GSE92281,GSE51280,GSE133987,GSE56443,GSE66387,GSE76360" q5
#python3 prepareQueryData.py "GSE25765,GSE16199,GSE25768,GSE16499,GSE49937,GSE24110,GSE136308,GSE145808,GSE120020,GSE61787,GSE2236,GSE32936,GSE28031,GSE3530,GSE145697,GSE63848,GSE19210,GSE26887,GSE43932,GSE76593,GSE68857,GSE62973,GSE13336,GSE17363,GSE6662,GSE29145,GSE37047,GSE16790" q6

#corpusMaxSize=1000000
corpusMaxSize=100

#for numKeywords in 10 20 30
for numKeywords in 10
do
  python3 runSciSpacy.py $numKeywords 200 $corpusMaxSize
  #python3 runBioWordVec.py  
  #python3 runFastTextWiki.py
  #python3 runSpacy.py
  #python3 runFastTextSKIPGRAM.py     
  #python3 runFastTextCBOW.py
done

#python3 getResults.py
