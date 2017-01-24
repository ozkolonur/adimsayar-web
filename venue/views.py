# -*- coding: utf-8 -*-
from django.http import HttpResponse
import urllib
import simplejson as json
from django.shortcuts import render_to_response
from venue.models import Venue, VenueCategory, Checkin, VenueSerializer
import urllib, urllib2
from django.core import serializers
from django.utils import simplejson

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

#resp = 'TR,34,Istanbul,,41.018600,28.964701,0,0,"Hosting Internet Hizmetleri Ltd Sti","Mars-Customer"'
def get_client_coordinates(ipaddr):
    url = 'http://geoip3.maxmind.com/f?l=AXWmumf9WxvE&i='+ipaddr
    page = urllib2.urlopen(url)
    resp = page.readlines()[0]
    location=resp.split(',')
    isp_unquote = location[8]

    error = False

    if location[4] == "":
        error = True
    else:
        lon = location[4]

    if location[5] == "":
        error = True
    else:
        lat = location[5]

    if error:
        return None
    return lon,lat


def fs_query(ll, near, radius, intent, query):
    oauth_token = "5WS0DMWY1EGYNNQQDDQLJJKTRAXKQ32JPAFO0OTUL1H3B0IX"
    v = "20120608"
    #if precise intent=checkin else browse
    limit = '49'
    categories = ('4bf58dd8d48988d175941735,'+
                   '4d4b7105d754a06377d81259,'+
                   '4f4528bc4b90abdf24c9de85,'+
                   '4cce455aebf7b749d5e191f5,'+
                   '4e39a956bd410d7aed40cbc3,'+
                   '4eb1bf013b7b6f98df247e07,')

    params = ( dict(oauth_token=oauth_token, v=v, radius=radius, 
                        query=query, intent=intent, limit=limit) )

    if near:
        params['near'] = near
    elif ll:
        params['ll'] = ll
    else:
        return None

    venues = None

    try:
        full_resp = urllib.urlopen("https://api.foursquare.com/v2/venues/search?" + 
                      urllib.urlencode(params))
        resp = json.load(full_resp)
        response = resp['response']
        venues = response['venues']
    except Exception,err:
        return None

    return venues

#   fs sorgu yap
#   her sorgu sonucu icin get_or_create
#   sonuclari query formatinda al
#   siralama yap
#   render et

def fs_get_venues(ll, near, intent="browse", precise=False):
    if intent == "checkin":
        radius = "800"
    elif intent == "browse":
        radius = "100000"
    query = fs_query(ll, near, radius, intent, query="Spor")
    venues = query
    query = fs_query(ll, near, radius, intent, query="Gym")
    venues += query
    query = fs_query(ll, near, radius, intent, query="Salad")
    venues += query
    query = fs_query(ll, near, radius, intent, query="Salata")
    venues += query
    query = fs_query(ll, near, radius, intent, query="Park")
    to_remove = []
    for q in query:
       try:
           cat = q['categories'][0]['name']
           if cat == "Parking":
               to_remove.append(q)
       except Exception, err:
           continue
    for q in to_remove:
       query.remove(q)
    venues += query
    return venues

def get_venues(json_venues):
    #TODO
    obj_venues = []
    for ven in json_venues:
        try:
            venue, created = Venue.objects.get_or_create(venue_id = ven['id'])
            if created:
                name_str = ven['name']
                venue.name = name_str

                try:
                    venue.lat = ven['location']['lat']
                    venue.lon = ven['location']['lng']
                except:
                    pass

                try:
                    cat_str = ven['categories'][0]['name']
                    category, created = VenueCategory.objects.get_or_create(name=cat_str)
                    icon_pre = ven['categories'][0]['icon']['prefix']
                    icon_suf = ven['categories'][0]['icon']['name']
                    icon_sizes = ven['categories'][0]['icon']['sizes']
                    icon_size = None
                    if 64 in icon_sizes:
                        icon_size = "32"
                    icon = icon_pre + icon_size + icon_suf
                    if created:
                        category.icon = icon
                        category.save()
                    venue.icon = icon
                    venue.category = category
                except Exception,err:
                    print str(err)
                    pass
                venue.save()
            obj_venues.append(venue)
            #print v['id'] + ":" + v['categories'][0]['name']
        except Exception,err:
            print str(err)
            continue
    return obj_venues

def sort_venues(venues):
    #TODO
    return venues

def list(request):
    lon = request.GET.get('lon', None)
    lat = request.GET.get('lat', None)
    prec = request.GET.get('precise', None)
    if prec:
        precise = True

    if lon and lat:
        intent = "checkin"
    else:
        intent = "browse"
        ip_addr = get_client_ip(request)
        lon, lat = get_client_coordinates(ip_addr)

    ll = lon+","+lat
    #fulya:ll="41.052598269905744,29.001865594266413"
    #gaziantep:ll="37.07747097276475,37.33467599436948"
    json_venues = fs_get_venues(near=None, ll=ll, intent=intent, precise=False)
    venues = get_venues(json_venues)
    venues_sorted = sort_venues(venues)
#    return render_to_response('checkin/venues_list.json',{ 'venues': venues_sorted, 'll':ll, 'intent':intent })
    #serializer = VenueSerializer()
    data = serializers.serialize('json', venues_sorted)
    return HttpResponse(data, mimetype='application/json')
    data = []
    for v in venues_sorted:
        d = dict()
        d['name'] = v.name
        d['icon'] = v.icon
        d['description'] = "Bu bir description"
        d['point'] = v.points
        data.append(d)
    response = simplejson.dumps(data)
    return HttpResponse(response, mimetype='application/json')

def checkin(request):
    venue_id = request.GET.get("venue_id")
    return HttpResponse(venue_id)
