#!/bin/bash

FILE=/Data/concept_model.bin

if [ ! -f "$FILE" ]; then
    wget -O ${FILE} https://ftp.ncbi.nlm.nih.gov/pub/lu/BioConceptVec/bioconceptvec_fasttext.bin
fi    
