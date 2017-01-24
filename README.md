
Adimsayar initially developed as a mobile application as fitness pedometer. 
Soon we have created a web service you can analyze walking habits.
Soon we added many content on this web application developed using python django.
We shared source code in order other people can use it or pick pieces his/her needs.
It is in Turkish but translations possible using already implemented translation text files.

We are also planning to open-source mobile applications.


Here is howto setup and install it

$ sudo apt-get install python-virtualenv
$ cd /path/to/adimsayar
$ virtualenv .
(virtual) $ pip install -r requirements.txt


Proxy configuration of Adimsayar

copy adimsayar.com.conf /etc/apache2/sites-available     (I will add it soon)
a2ensite adimsayar.com
service apache2 reload



![Alt text](https://github.com/ozkolonur/adimsayar-web/blob/master/screenshots/adimsayar-main.png?raw=true "Homepage")
![Alt text](https://github.com/ozkolonur/adimsayar-web/blob/master/screenshots/adimsayar-weight.png?raw=true "Weight Management")
![Alt text](https://github.com/ozkolonur/adimsayar-web/blob/master/screenshots/adimsayar-step.png?raw=true "Step Graphs")

