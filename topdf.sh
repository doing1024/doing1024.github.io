#!/bin/zsh
pandoc --pdf-engine=xelatex -V CJKmainfont="WenQuanYi Micro Hei" ${1} -o ${1%.*}.pdf

