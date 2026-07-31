#!/bin/bash

libreoffice --headless --convert-to pdf --outdir ./media/presentation ./media/presentation/Helium.odp

cd ./media/paper && pdflatex main.tex && bibtex main && pdflatex main.tex && pdflatex main.tex && cd ../../

mv ./media/paper/main.pdf ./media-builds/
mv ./media/presentation/Helium.pdf ./media-builds/