# -*- coding: utf-8 -*-
import os
import sys

heads, tail = os.path.split(os.path.dirname(os.path.abspath(__file__)))
site_root, project_dir_name = os.path.split(heads)
sys.path.append(heads)

os.environ['PROJECT_DIR_NAME'] = project_dir_name
os.environ['DJANGO_SETTINGS_MODULE'] = project_dir_name + '.settings'
os.environ['OVERLOAD_SITE'] = 'adimsayar'
os.environ['SITE_ROOT'] = os.path.dirname(__file__)

from django.core.management import setup_environ
import settings

setup_environ(settings)
DEBUG = False

#keep this for render_to_string unicode errors
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from django.template.loader import render_to_string
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
from datetime import datetime,timedelta
from core.models import Profile
from statistics.models import DailyStatistics
from django.core.cache import cache
from meas.models import *
import time, cgi, urllib, urllib2
from django.http import HttpResponse
from core.models import Location, Country, City, Isp
# Create your views here.


COUNTRY_CODES = (
    '', 'AP', 'EU', 'AD', 'AE', 'AF', 'AG', 'AI', 'AL', 'AM', 'AN', 'AO', 'AQ',
    'AR', 'AS', 'AT', 'AU', 'AW', 'AZ', 'BA', 'BB', 'BD', 'BE', 'BF', 'BG', 'BH',
    'BI', 'BJ', 'BM', 'BN', 'BO', 'BR', 'BS', 'BT', 'BV', 'BW', 'BY', 'BZ', 'CA',
    'CC', 'CD', 'CF', 'CG', 'CH', 'CI', 'CK', 'CL', 'CM', 'CN', 'CO', 'CR', 'CU',
    'CV', 'CX', 'CY', 'CZ', 'DE', 'DJ', 'DK', 'DM', 'DO', 'DZ', 'EC', 'EE', 'EG',
    'EH', 'ER', 'ES', 'ET', 'FI', 'FJ', 'FK', 'FM', 'FO', 'FR', 'FX', 'GA', 'GB',
    'GD', 'GE', 'GF', 'GH', 'GI', 'GL', 'GM', 'GN', 'GP', 'GQ', 'GR', 'GS', 'GT',
    'GU', 'GW', 'GY', 'HK', 'HM', 'HN', 'HR', 'HT', 'HU', 'ID', 'IE', 'IL', 'IN',
    'IO', 'IQ', 'IR', 'IS', 'IT', 'JM', 'JO', 'JP', 'KE', 'KG', 'KH', 'KI', 'KM',
    'KN', 'KP', 'KR', 'KW', 'KY', 'KZ', 'LA', 'LB', 'LC', 'LI', 'LK', 'LR', 'LS',
    'LT', 'LU', 'LV', 'LY', 'MA', 'MC', 'MD', 'MG', 'MH', 'MK', 'ML', 'MM', 'MN',
    'MO', 'MP', 'MQ', 'MR', 'MS', 'MT', 'MU', 'MV', 'MW', 'MX', 'MY', 'MZ', 'NA',
    'NC', 'NE', 'NF', 'NG', 'NI', 'NL', 'NO', 'NP', 'NR', 'NU', 'NZ', 'OM', 'PA',
    'PE', 'PF', 'PG', 'PH', 'PK', 'PL', 'PM', 'PN', 'PR', 'PS', 'PT', 'PW', 'PY',
    'QA', 'RE', 'RO', 'RU', 'RW', 'SA', 'SB', 'SC', 'SD', 'SE', 'SG', 'SH', 'SI',
    'SJ', 'SK', 'SL', 'SM', 'SN', 'SO', 'SR', 'ST', 'SV', 'SY', 'SZ', 'TC', 'TD',
    'TF', 'TG', 'TH', 'TJ', 'TK', 'TM', 'TN', 'TO', 'TL', 'TR', 'TT', 'TV', 'TW',
    'TZ', 'UA', 'UG', 'UM', 'US', 'UY', 'UZ', 'VA', 'VC', 'VE', 'VG', 'VI', 'VN',
    'VU', 'WF', 'WS', 'YE', 'YT', 'RS', 'ZA', 'ZM', 'ME', 'ZW', 'A1', 'A2', 'O1',
    'AX', 'GG', 'IM', 'JE', 'BL', 'MF'
    )

COUNTRY_NAMES = (
    "unknown", "Asia/Pacific Region", "Europe", "Andorra", "United Arab Emirates",
    "Afghanistan", "Antigua and Barbuda", "Anguilla", "Albania", "Armenia",
    "Netherlands Antilles", "Angola", "Antarctica", "Argentina", "American Samoa",
    "Austria", "Australia", "Aruba", "Azerbaijan", "Bosnia and Herzegovina",
    "Barbados", "Bangladesh", "Belgium", "Burkina Faso", "Bulgaria", "Bahrain",
    "Burundi", "Benin", "Bermuda", "Brunei Darussalam", "Bolivia", "Brazil",
    "Bahamas", "Bhutan", "Bouvet Island", "Botswana", "Belarus", "Belize",
    "Canada", "Cocos (Keeling) Islands", "Congo, The Democratic Republic of the",
    "Central African Republic", "Congo", "Switzerland", "Cote D'Ivoire", "Cook Islands",
    "Chile", "Cameroon", "China", "Colombia", "Costa Rica", "Cuba", "Cape Verde",
    "Christmas Island", "Cyprus", "Czech Republic", "Germany", "Djibouti",
    "Denmark", "Dominica", "Dominican Republic", "Algeria", "Ecuador", "Estonia",
    "Egypt", "Western Sahara", "Eritrea", "Spain", "Ethiopia", "Finland", "Fiji",
    "Falkland Islands (Malvinas)", "Micronesia, Federated States of", "Faroe Islands",
    "France", "France, Metropolitan", "Gabon", "United Kingdom",
    "Grenada", "Georgia", "French Guiana", "Ghana", "Gibraltar", "Greenland",
    "Gambia", "Guinea", "Guadeloupe", "Equatorial Guinea", "Greece",
    "South Georgia and the South Sandwich Islands",
    "Guatemala", "Guam", "Guinea-Bissau",
    "Guyana", "Hong Kong", "Heard Island and McDonald Islands", "Honduras",
    "Croatia", "Haiti", "Hungary", "Indonesia", "Ireland", "Israel", "India",
    "British Indian Ocean Territory", "Iraq", "Iran, Islamic Republic of",
    "Iceland", "Italy", "Jamaica", "Jordan", "Japan", "Kenya", "Kyrgyzstan",
    "Cambodia", "Kiribati", "Comoros", "Saint Kitts and Nevis",
    "Korea, Democratic People's Republic of",
    "Korea, Republic of", "Kuwait", "Cayman Islands",
    "Kazakstan", "Lao People's Democratic Republic", "Lebanon", "Saint Lucia",
    "Liechtenstein", "Sri Lanka", "Liberia", "Lesotho", "Lithuania", "Luxembourg",
    "Latvia", "Libyan Arab Jamahiriya", "Morocco", "Monaco", "Moldova, Republic of",
    "Madagascar", "Marshall Islands", "Macedonia",
    "Mali", "Myanmar", "Mongolia", "Macau", "Northern Mariana Islands",
    "Martinique", "Mauritania", "Montserrat", "Malta", "Mauritius", "Maldives",
    "Malawi", "Mexico", "Malaysia", "Mozambique", "Namibia", "New Caledonia",
    "Niger", "Norfolk Island", "Nigeria", "Nicaragua", "Netherlands", "Norway",
    "Nepal", "Nauru", "Niue", "New Zealand", "Oman", "Panama", "Peru", "French Polynesia",
    "Papua New Guinea", "Philippines", "Pakistan", "Poland", "Saint Pierre and Miquelon",
    "Pitcairn Islands", "Puerto Rico", "Palestinian Territory",
    "Portugal", "Palau", "Paraguay", "Qatar", "Reunion", "Romania",
    "Russian Federation", "Rwanda", "Saudi Arabia", "Solomon Islands",
    "Seychelles", "Sudan", "Sweden", "Singapore", "Saint Helena", "Slovenia",
    "Svalbard and Jan Mayen", "Slovakia", "Sierra Leone", "San Marino", "Senegal",
    "Somalia", "Suriname", "Sao Tome and Principe", "El Salvador", "Syrian Arab Republic",
    "Swaziland", "Turks and Caicos Islands", "Chad", "French Southern Territories",
    "Togo", "Thailand", "Tajikistan", "Tokelau", "Turkmenistan",
    "Tunisia", "Tonga", "Timor-Leste", "Turkey", "Trinidad and Tobago", "Tuvalu",
    "Taiwan", "Tanzania, United Republic of", "Ukraine",
    "Uganda", "United States Minor Outlying Islands", "United States", "Uruguay",
    "Uzbekistan", "Holy See (Vatican City State)", "Saint Vincent and the Grenadines",
    "Venezuela", "Virgin Islands, British", "Virgin Islands, U.S.",
    "Vietnam", "Vanuatu", "Wallis and Futuna", "Samoa", "Yemen", "Mayotte",
    "Serbia", "South Africa", "Zambia", "Montenegro", "Zimbabwe",
    "Anonymous Proxy","Satellite Provider","Other",
    "Aland Islands","Guernsey","Isle of Man","Jersey","Saint Barthelemy","Saint Martin"
    )


#resp = 'TR,34,Istanbul,,41.018600,28.964701,0,0,"Hosting Internet Hizmetleri Ltd Sti","Mars-Customer"'
def get_client_location(ipaddr):
	url = 'http://geoip3.maxmind.com/f?l=AXWmumf9WxvE&i='+ipaddr
	page = urllib2.urlopen(url)
	resp = page.readlines()[0]
	print resp
	location=resp.split(',')
	isp_unquote = location[8]

	if location[2] == "":
		city = "unknown"
	else:
		city = location[2]

	if isp_unquote[1:-1] == "":
		isp = "unknown"
	else:
		isp = isp_unquote[1:-1]

	return location[0], city, isp

def update_user_location(profile):
	tmp_country_code, tmp_city, tmp_isp = get_client_location(profile.ip_addr)
	print 'country='+tmp_country_code+' city='+tmp_city+' isp='+tmp_isp
	isp,created = Isp.objects.get_or_create(name=tmp_isp)
	tmp_country = country_names[tmp_country_code]
	country,created = Country.objects.get_or_create(name=tmp_country, shortcode=tmp_country_code)
	city, created = City.objects.get_or_create(name=tmp_city,country=country)
	location  = Location.objects.filter(country=country, city=city)
	if len(location) == 0:
		location = Location(country=country, city=city)
		location.save()
		profile.user_location = location
		profile.isp = isp
	else:
		profile.user_location = location[0]
		profile.isp = isp
	profile.save()
	return True

country_names_tuple = zip(COUNTRY_CODES, COUNTRY_NAMES)
country_names = dict(country_names_tuple)
users = User.objects.all()
for user in users:
	try:
		if user.email == 'admin@admin.com':
			continue
		profile = Profile.objects.get(user=user)
		if profile.user_location == None:
			#print 'ip_addr was:' + profile.ip_addr + ' len=' + str(len(profile.ip_addr)) 
			if (len(profile.ip_addr) > 5):
				update_user_location(profile)
				print 'location updated: ' + user.email
			else:
				continue
	except:
		#print "EXCEPTION" + user.email
		pass

'''
users = User.objects.all()
for user in users:
	try:
		profile = Profile.objects.get(user=user)
	except:
		continue
	profile.user_location = None
	profile.isp = None
	profile.save()
'''
#countries = Country.objects.all()
#for country in countries:
#	country.shortcode = country.name
#	country.name = country_names[country.shortcode]
#	country.save()
