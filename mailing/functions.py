# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from datetime import datetime, timedelta,time
from meas.models import Step
from ad.models import Ad
from poll.models import Question, Answer
from mailing.models import Mailing, Element
from core.models import Profile
from django.core.urlresolvers import reverse
from django.conf import settings
from badges.models import Badge
from body_info.models import BodyInfo
import ast
import md5
import hashlib

def mail_weekly_steps_params(**params):
    email = params['email']
    user = params['user']
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
    return {'step_list': step_list, 'total_steps': total_steps,'daily_average_steps':daily_average_steps, 'daily_average_calories':daily_average_calories}


def calc_bmi(profile):
    if profile.height == 0:
        return None
    if not profile.height:
        return None
    res = (profile.weight / 
        ((profile.height/100.00) * (profile.height/100.00)))
    if res > 0 and res < 50:
        return "%.2f" % res
    else:
        return None

URL_VALIDATOR_SECRET = 'azim'

def add_validator(url):
    #TODO sanity check
    key = url+ '|' + URL_VALIDATOR_SECRET
    mail_key = hashlib.md5(key).hexdigest()
    return url + "&v=" + mail_key

def check_validator(request):
    url = request.build_absolute_uri()
    v = request.GET.get('v',None)
    if not v:
        return False
    target_url = url[:-35]
    secret = target_url + "|" + URL_VALIDATOR_SECRET
    v_request =hashlib.md5(secret).hexdigest()
    if v == v_request:
        return True
    else:
        return False

def mail_poll_params(**params):
    email = params['email']
    user = params['user']
    element = params['element']
    extra_params = ast.literal_eval(element.params)
    poll_id = extra_params['poll_id']
    question = Question.objects.get(id=poll_id)
    answers = Answer.objects.filter(question=question)
    ans_base_url = 'http://' + settings.DOMAIN_NAME + '/poll/result/' + str(poll_id) + '/?a=1&utm_source=weekly_mail&utm_medium=email&utm_campaign=mail_poll'
    answer_url = add_validator(ans_base_url)
    answer_links = []
    # key=f(email, answer_url, salt
    for answer in answers:
        link = (ans_base_url + '&answer=' + str(answer.id) +  
            '&key_id=' + str(user.id))
        link = add_validator(link)
        answer_links.append(link)

    return { 'question':question, 'answers':answers, 
        'answer_links':answer_links, 'answer_url':answer_url }

def mail_won_badge_params(**params):
    email = params['email']
    user = params['user']
    element = params['element']
    extra_params = ast.literal_eval(element.params)
    badge_id = extra_params['badge_id']
    badge = Badge.objects.get(id=badge_id)
    return { 'badge':badge }


def mail_bmi_meter_params(**params):
    email = params['email']
    user = params['user']
    result = ""
    try:
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

    return { 'cur_bmi':cur_bmi, 'bmi_img_url':bmi_img_url }

def mail_header_params(**params):
    email = params['email']
    user = params['user']
    mailing_id = params['mailing_id']

    #TODO:we should add a key later
    tracker_img = "http://" + settings.DOMAIN_NAME + "/mailing/tracking_img/"+str(user.id)+"/"+str(mailing_id)+"/"
    logo_img = "http://" + settings.DOMAIN_NAME + "/site_media/images/logo72_adimsayar.png"

    mailing = Mailing.objects.get(id=mailing_id)
    title = None
    if mailing.get_mail_type_display() == "weekly":
        title = u'Haftalık Rapor'
    elif mailing.get_mail_type_display() == "weight_update":
        title = u'Hatırlatma'
    elif mailing.get_mail_type_display() == "won_badge":
        title = u'Tebrikler'

    return { 'tracker_img':tracker_img, 'logo_img':logo_img, 'title':title, 'email':email }

def mail_footer_params(**params):
    email = params['email']
    user = params['user']
    mailing_id = params['mailing_id']

    #TODO:we should add a key later

    mailing = Mailing.objects.get(id=mailing_id)

    send_mail_url = ('http://'+ settings.DOMAIN_NAME +'/profile/send_mail/?email='+ email +
                     '&mail_type='+ mailing.get_mail_type_display() +'&key=' + '29345434')
    user_delete_url = ('http://'+ settings.DOMAIN_NAME +'/profile/user_delete/?email=' + email +
                     '&key=' + '29345434')
    new_password_url = ('http://' + settings.DOMAIN_NAME +'/mining_platform/reset_password_email/?email='+ email + 
                        '&key=' + '5565233909')
    contact_url = ('http://'+ settings.DOMAIN_NAME + '/contact/')
    return { 'send_mail_url':send_mail_url, 'user_delete_url':user_delete_url, 
             'new_password_url':new_password_url, 'contact_url':contact_url }

def mail_weight_update_params(**params):
    email = params['email']
    user = params['user']
    mailing_id = params['mailing_id']

    body_infos = BodyInfo.objects.filter(user=user).order_by('-date_time')
    if len(body_infos) > 0:
        latest = body_infos[0].date_time
        today = datetime.now()
        days = today - latest
        since = str(days.days)
    else:
        since = "45"
    return { 'since':since }

def mail_score_params(**params):
    email = params['email']
    user = params['user']
    mailing_id = params['mailing_id']

    body_infos = BodyInfo.objects.filter(user=user).order_by('-date_time')
    if len(body_infos) > 0:
        latest = body_infos[0].date_time
        today = datetime.now()
        days = today - latest
        since = str(days.days)
    else:
        since = "45"
    return { 'rank':121 }

def mail_ad_params(**params):
    email = params['email']
    user = params['user']
    mailing_id = params['mailing_id']
    #1.hafta
    #cift numara termal_kemer
    #tek numara abtronic_x2

    #2.hafta
    #cift numara abtronic_x2
    #tek numara tefal

    #3.hafta
    #cift numara ba_fat_magnet
    #tek numara ba_termal_kemer

    #4. hafta
    #visco yatak
    #tek numara ba_termal_kemer
    if (user.id % 2 == 0):
        ad_name = 'ba_sisli_active_gym'
    else:
        ad_name = 'ba_sisli_active_gym'

    #TODO: match ad and user using tags
    try:
        profile = Profile.objects.get(user=user)
        if profile.user_location.city.name == u'Istanbul':
            ad_name = 'ba_galata_alman_checkup'
#            ad_name = 'ba_sisli_active_gym'
#            ad_name = 'ba_alpha_tip'
#            ad_name = 'ba_gida_intolerans'
    except:
        pass

    ad = Ad.objects.get(name=ad_name)
    ad.impression += 1
    ad.save()
    ad_text = ad.text
    return { 'text':ad_text }



functionList = { 
    'mail_weekly_steps_params': mail_weekly_steps_params,
    'mail_poll_params': mail_poll_params,
    'mail_weight_update_params': mail_weight_update_params,
    'mail_score_params': mail_score_params,
    'mail_won_badge_params': mail_won_badge_params,
    'mail_bmi_meter_params': mail_bmi_meter_params,
    'mail_header_params': mail_header_params,
    'mail_footer_params': mail_footer_params,
    'mail_ad_params': mail_ad_params,
}
