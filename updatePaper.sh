#!/bin/bash


./build/build.sh
manubot webpage
cd ./webpage
python -m http.server
