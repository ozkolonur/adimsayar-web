#!/bin/sh

s3cmd get s3://adimsayar-backup/adimsayar.org-`date --date=yesterday +%Y-%m-%d`.sql.gz /tmp
mysql -u root -ppassword -e "drop database adimsayar_biz;"
mysql -u root -ppassword -e "create database adimsayar_biz;"
gunzip /tmp/adimsayar.org-`date --date=yesterday +%Y-%m-%d`.sql.gz
mysql -u root -ppassword -h localhost adimsayar_biz < /tmp/adimsayar.org-`date --date=yesterday +%Y-%m-%d`.sql
rm /tmp/adimsayar.org-`date --date=yesterday +%Y-%m-%d`.sql
svn up /home/ubuntu/adimsayar_biz
python /home/ubuntu/adimsayar_biz/manage.py syncdb
