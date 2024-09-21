#!/bin/sh

# 监视的文件或目录
filename=./

# 监视发现有增、删、改时执行的脚本
script=build.sh

inotifywait -mrq --format '%e' --event create,delete,modify  $filename | while read event
do
    case $event in MODIFY|CREATE|DELETE) bash $script ;;
    esac
done
