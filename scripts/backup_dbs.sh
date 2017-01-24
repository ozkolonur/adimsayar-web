#!/bin/sh

suffix=$(date +%w%a)
#rm /tmp/$suffix.sql.gz
mysqldump adimsayar -u root -pKoper900 | gzip > /home/ubuntu/backup/adimsayar.org-`date +%Y-%m-%d`.sql.gz
nice -n19 s3cmd put /home/ubuntu/backup/adimsayar.org-`date +%Y-%m-%d`.sql.gz s3://adimsayar-backup
rm /home/ubuntu/backup/adimsayar.org-`date +%Y-%m-%d`.sql.gz
