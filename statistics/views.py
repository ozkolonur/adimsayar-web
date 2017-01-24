# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.contrib.auth.models import User
from core.models import Profile
from content.models import Content
from statistics.models import AgeVsUser
from statistics.models import BmiVsUser
from django.http import HttpResponse,HttpResponseRedirect, HttpResponsePermanentRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext, loader
from statistics.models import DailyStats

def index(request):
    return render_to_response('statistics/index.html',{'user':request.user})


def bmi_index(request):
    """
    mailden gelen kullanicilar icin bmi index sayfasi
    """
    if request.method == 'POST':
        bmi_height = request.POST.get('bmi_height','')
        bmi_weight = request.POST.get('bmi_weight','')
        bmi_age = request.POST.get('bmi_age','')
        try:
            bmi_height = int(bmi_height)
            bmi_weight = int(bmi_weight)
            bmi_age = int(bmi_age)
        except:
            error = u'Lütfen değerlerinizi sayı olarak giriniz.'
            return render_to_response('statistics/bmi_register.html',
          			{'error':error ,'user':request.user },context_instance=RequestContext(request))

        profile = Profile.objects.filter(user = request.user)
        profile.update(
            height = bmi_height,
            weight = bmi_weight,
            age =  bmi_age,
        )

        profile = profile[0]
        bmi = (profile.weight / ((profile.height/100.00) * (profile.height/100.00)))
        bmi = '%.2f' % bmi
        return render_to_response('statistics/bmi_meter_widget.html',
      			{'bmi':bmi,'user':request.user},context_instance=RequestContext(request))


    if request.user.is_authenticated():  #uye girisi yapildimi
        profile, created = Profile.objects.get_or_create(user=request.user)
        try:
            content = Content.objects.get(page="bmi_warning")
            if   profile.height > 0 : #degerler varmi bak
               bmi = (profile.weight / ((profile.height/100.00) * (profile.height/100.00)))
               bmi =  "%.2f" % bmi
               return render_to_response('statistics/bmi_meter_widget.html',
              			{'bmi':bmi,'user':request.user},context_instance=RequestContext(request))
            else:  #yoksa girmesini iste
               return render_to_response('statistics/bmi_register.html',
              			{'user':request.user},context_instance=RequestContext(request))
        except Exception,err :#sadece user giris durumu varsa profile yoksa kayıt al
            return HttpResponseRedirect('/accounts/login/?next=/statistics/my_bmi/')

    else: #register kayit
        return HttpResponseRedirect('/accounts/login/?next=/statistics/my_bmi/')


def bmi_tool(request):
    """
    mailden gelen kullanicilar icin bmi index sayfasi
    """
    if request.method == 'POST':
        bmi_height = request.POST.get('bmi_height','')
        bmi_weight = request.POST.get('bmi_weight','')
        bmi_age = request.POST.get('bmi_age','')
        try:
            bmi_height = int(bmi_height)
            bmi_weight = int(bmi_weight)
            bmi_age = int(bmi_age)
        except:
            error = u'Lütfen değerlerinizi sayı olarak giriniz.'
            return render_to_response('statistics/bmi_register.html',
          			{'error':error ,'user':request.user },context_instance=RequestContext(request))

        profile = Profile.objects.filter(user = request.user)
        profile.update(
            height = bmi_height,
            weight = bmi_weight,
            age =  bmi_age,
        )

        profile = profile[0]
        bmi = (profile.weight / ((profile.height/100.00) * (profile.height/100.00)))
        bmi = '%.2f' % bmi
        return render_to_response('statistics/bmi_tool.html',
      			{'bmi':bmi,'user':request.user},context_instance=RequestContext(request))


    if request.user.is_authenticated():  #uye girisi yapildimi
        profile, created = Profile.objects.get_or_create(user=request.user)
        try:
            content = Content.objects.get(page="bmi_warning")
            if   profile.height > 0 : #degerler varmi bak
               bmi = (profile.weight / ((profile.height/100.00) * (profile.height/100.00)))
               bmi =  "%.2f" % bmi
               return render_to_response('statistics/bmi_tool.html',
              			{'bmi':bmi,'user':request.user},context_instance=RequestContext(request))
            else:  #yoksa girmesini iste
               return render_to_response('statistics/bmi_register.html',
              			{'user':request.user},context_instance=RequestContext(request))
        except Exception,err :#sadece user giris durumu varsa profile yoksa kayıt al
            return HttpResponseRedirect('/accounts/login/?next=/statistics/bmi_tool/')

    else: #register kayit
        return HttpResponseRedirect('/accounts/login/?next=/statistics/bmi_tool')


def age_vs_user(request):
    latest = AgeVsUser.objects.latest('stat_time').stat_time
    age_vs_user = AgeVsUser.objects.filter(age__gt=10, age__lt=66, stat_time__gt=latest.strftime("%Y-%m-%d"))
    return render_to_response('statistics/age-vs-user.html',{"age_vs_user":age_vs_user})

def bmi_vs_user(request):
    latest = BmiVsUser.objects.latest('stat_time').stat_time
    bmi_vs_user = BmiVsUser.objects.filter(stat_time__gt=latest.strftime("%Y-%m-%d"))
    return render_to_response('statistics/bmi-vs-user.html',{"bmi_vs_user":bmi_vs_user})

def avg_daily_stepcount(request):
    bmi_vs_user = BmiVsUser.objects.all()
    return render_to_response('statistics/bmi-vs-user.html',{"bmi_vs_user":bmi_vs_user})

def age_vs_provinces(request):
    latest = BmiVsUser.objects.latest('stat_time').stat_time
    bmi_vs_user = BmiVsUser.objects.filter(stat_time__gt=latest.strftime("%Y-%m-%d"))
    return render_to_response('statistics/age_vs_provinces.html',{"bmi_vs_user":bmi_vs_user})

def daily_stats(request):
    if not request.user.is_superuser:
        return HttpResponseRedirect('/')
    stats = DailyStats.objects.all()
    return render_to_response('statistics/daily_stats.html',
        {"stats":stats},context_instance=RequestContext(request))






