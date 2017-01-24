#!/bin/sh

suffix=$(date +%w%a)
#rm /tmp/$suffix.sql.gz
nice -n19 tar cpzf /home/ubuntu/backup/backup-image-`date +%Y-%m-%d`.tgz --exclude=/proc --exclude=/lost+found --exclude=/home/ubuntu/backup --exclude=/mnt --exclude=/sys --exclude=/dev --exclude=/etc/hostname --exclude=/mnt/adimsayar-backup --exclude=/etc/hosts /
nice -n19 s3cmd put /home/ubuntu/backup/backup-image-`date +%Y-%m-%d`.tgz s3://adimsayar-backup
rm /home/ubuntu/backup/backup-image-`date +%Y-%m-%d`.tgz