#!/bin/sh

rm -Rf /tmp/adimsayar-android
svn co http://ferlin.unfuddle.com/svn/ferlin_doktorfil/adimsayar-android /tmp/adimsayar-android
#cp /tmp/adimsayar-android/assets_src/download_html.sh /tmp/adimsayar-android/download_html.sh
/tmp/adimsayar-android/download_html.sh android
cd /tmp/adimsayar-android
ant release
cp /tmp/adimsayar-android/bin/mainActivity-release.apk /home/ubuntu/adimsayar/media/images/adimsayar-nightly-`date +%Y-%m-%d`.apk
/home/ubuntu/adimsayar/bin/python /home/ubuntu/adimsayar/manage.py send_mail ozkolonur@gmail.com,erdemozkol@gmail.com Adimsayar-BuildRobot NightlyBuild-android:http://www.adimsayar.com/site_media/images/adimsayar-nightly-`date +%Y-%m-%d`.apk
