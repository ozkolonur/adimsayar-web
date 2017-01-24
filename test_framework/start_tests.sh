#!/bin/sh

DIR=`dirname $0`
/home/ubuntu/adimsayar/bin/python /home/ubuntu/adimsayar/manage.py del_user adimsayarmonk2@gmail.com
for srcfile in `ls ${DIR} | grep -v start_tests.sh`; do
    /home/ubuntu/adimsayar/bin/python ${DIR}/${srcfile}
done

