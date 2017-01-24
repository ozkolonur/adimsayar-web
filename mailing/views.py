# -*- coding: utf-8 -*-
# Create your views here.
from django.http import HttpResponse,HttpResponseRedirect
from meas.models import *
from django.contrib.auth.models import User
from datetime import datetime, timedelta,time
from django.shortcuts import render_to_response
from django.template.loader import render_to_string
from body_info.views import get_bmi_widget
from meas.views import get_weekly_steps
from django.conf import settings
from core.models import Profile
from django.template import RequestContext, loader
from content.models import Content
from django.template import Context, Template
from mailing.models import Mailing, Element, UserReadMail
from mailing.functions import *
import json

def mailing_index(request):
    #if not request.user.is_superuser:
    #    return HttpResponseRedirect('/')

    mailing_id = 53

    if request.method == 'POST':
        mailing_id = request.POST.get('mailing_id','')

    mailings = Mailing.objects.all()
    return render_to_response('mailing/index.html',
        { 'mailings': mailings, 'mailing_id':mailing_id },
        context_instance=RequestContext(request))


def preview(request, mailing_id):
    resp = prepare_mail_content('oseruygun34@hotmail.com', mailing_id)
    #resp = prepare_mail_content('ozkolonur@gmail.com', mailing_id)
#id:37785, email:alikus22@gmail.com,RESULT:SENT
    return HttpResponse(resp)


def prepare_mail_content(email,mailing_id):
    #std_params is passed to all functions in functions.py
    user = User.objects.get(email=email)
    std_params = { 'user' : user, 'email':email, 'mailing_id':mailing_id}

    mailing = Mailing.objects.get(id=mailing_id)

    content = []
    elements = Element.objects.filter(mailing=mailing).order_by('order')
    #TODO: verify function field before calling
    for element in elements:
        # Render every content, if we need some variables
        #  get it from functions.py
        ct = Content.objects.get(page=element.content)
        t = Template(ct.text)
        if (element.function != ""):
            std_params['element'] = element
            ctx_params = functionList[element.function](**std_params)
            all_params = dict(ctx_params.items() + std_params.items())
            c = Context(all_params)
        else:
            c = Context(std_params)
        ct.text = t.render(c)
        content.append(ct)
    return mailing.subject, render_to_string(mailing.template, {'content':content })


def prepare_weekly_email(email):
    user = User.objects.get(email=email)
    now = datetime.now()
    step_list=[]
    total_steps = 0
    calories = 0
    for day in range(1,8):
        that_day = now - timedelta(days=day)
        step = Step.objects.filter(user=user, date_time__year=that_day.year, date_time__month=that_day.month, date_time__day=that_day.day)
        if step.count() > 0:
            step_list.append(str(step[0].total/100))
            total_steps += int(step[0].total)
            calories += float(step[0].calories)
        else:
            step_list.append(str(0))
    daily_average_steps = total_steps / 7
    daily_average_calories = calories / 7
    result = ""
    try:
        user = User.objects.get(email=email)
        profile = Profile.objects.get(user=user)
    except:
        result = "FAIL"

    if result != "FAIL":
        bmi = calc_bmi(profile)

    bmi_prime = None
    divsw = None
    divsh = None
    result, bmi_img_url, cur_bmi = get_bmi_widget(bmi_prime, bmi, divsw, divsh)

    if result == "FAIL":
        cur_bmi = ""

    content = []
    ct = Content.objects.get(page="mail_fiziksel_aktivite_20")
    content.append(ct)
    ct = Content.objects.get(page="mail_weekly_steps")
    t = Template(ct.text)
    c = Context({'step_list': step_list, 'user': user,'total_steps': total_steps,'daily_average_steps':daily_average_steps, 'daily_average_calories':daily_average_calories})
    tmp_text = t.render(c)
    ct.text = tmp_text
    content.append(ct)
    ct = Content.objects.get(page="mail_video_yuruyus_oncesi_isinma")
    content.append(ct)


    return render_to_string('automatic_emails/weekly.html', { 'user': user, 'email':email, 'content':content, 'cur_bmi':cur_bmi, 'bmi_img_url':bmi_img_url })


def tracking_img(request, user_id, mailing_id): 
    key = request.GET.get("key", None)
    user = User.objects.get(id=user_id)
    mailing = Mailing.objects.get(id=mailing_id)
    user_read_mail,created = UserReadMail.objects.get_or_create(user=user, mailing=mailing)
    user_read_mail.save()
    return HttpResponse(None, content_type='image/gif')

def bounces(request): 
    return HttpResponse("OK")

def complaints(request): 
    example = '{"notificationType":"Complaint","complaint":{"complainedRecipients":[{"emailAddress":"ugurlu47@hotmail.com"}],"timestamp":"2012-06-27T14:50:33.000Z","feedbackId":"000001382e6c2499-72a5374e-c067-11e1-9a27-e3cd9e1b3e57-000000"},"mail":{"timestamp":"2012-05-28T11:09:27.000Z","source":"adimsayarbilgi@gmail.com","messageId":"000001379322e959-397e6d62-e1d4-4196-90b5-9201fe626412-000000","destination":["ugurlu47@hotmail.com"]}}'
    message = json.loads(example)
    complaints_num = len(message['complaint']['complainedRecipients'])
    return HttpResponse("OK")

