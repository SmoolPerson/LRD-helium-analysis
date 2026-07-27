#!/bin/bash

cd ..

wget $1 -O downloaded-data.zip

unzip downloaded-data.zip

mv downloaded-data.zip data/

rm downloaded-data.zip

