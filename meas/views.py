# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.core.mail import EmailMultiAlternatives
from meas.models import *
from content.models import Content
from core.models import Profile
from django.contrib.auth.models import User
from django.contrib import auth
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.http import HttpResponse,HttpResponseRedirect,HttpResponsePermanentRedirect
from django.template import RequestContext
from datetime import datetime, timedelta,time
from django.core.urlresolvers import reverse
from django.core.cache import cache
from django.conf import settings
import StringIO
from PIL import Image, ImageDraw, ImageFont 
import csv
import urllib
import simplejson as json
import random
import threading
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.models import User
from core.models import Profile
import base64,StringIO
from body_info.models import BodyInfo
from badges.models import Badge, BadgeToUser
from score.models import Point, UserScore
from score.views import get_user_ranking
from datetime import date
from device2.models import Device2, Product, Model, Manufacturer

def step_key_get_date(key):
    #raise eception
    if ((key[0] == 's') and (key[1] == 't')):
        return date(int(key[6:10]), int(key[4:6]), int(key[2:4]))
    else:
        return None

def steps_commit(user, device, step_key, step_value, am_value):
    is_today = False
    result = -1

    date_time = step_key_get_date(step_key)
    date_today = datetime.now()
    if ((date_time.day >= (date_today.day - 4)) and 
        (date_time.month == date_today.month) and 
        (date_time.year == date_today.year)):
        is_today = True

    sts = Step.objects.filter(user=user, date_time=date_time)
    if (len(sts) > 0):
        st = sts[0]
    else:
        st = Step(user=user, date_time = date_time)
    st.device2 = device
    st.steps2 = step_value
    st.am = am_value
    st.save()
    result = 0
    return is_today, result

def send_test_mail(*args, **kwargs):
	text_content = "hello thread"
	subject, from_email, to = 'Adimsayar Otomatik Rapor', 'adimsayarbilgi@gmail.com', "ozkolonur@gmail.com"
	msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
	msg.send()
	return None

def version(request):
	user = User.objects.get(email="ozkolonur@gmail.com")
	profile = Profile.objects.filter(user=user)
#	profile.update(send_mail=False)
	return HttpResponse(profile.user)
#	return render_to_response('profile/dont_mail.html',{'user':user,'content':content}, context_instance=RequestContext(request))

#	t = threading.Thread(target=send_test_mail, args=['honur'], kwargs={'fail_silently': True})
#	t.setDaemon(True)
#	t.start()
	return HttpResponse('1.0.1')

def mobil_exp(request):
	if request.user.is_authenticated():
		content = Content.objects.filter(page='warning')
		return render_to_response('meas/mobil_exp.html', {'content':content},context_instance=RequestContext(request))
	else:
		redirect_url = 'http://'+settings.DOMAIN_NAME+'/accounts/login?next=/meas/fbapp/'
		redirect_code = """
		<script type="text/javascript">
		top.location.href='%s';
		</script>
		""" % redirect_url;
		return HttpResponse(redirect_code,mimetype="text/html")

def steps_check(user):
     steps=Step.objects.filter(user=user)
     if len(steps)>0:
        return True
     else:
		return False

		
def meas_index(request):
    target = request.GET.get('target','points')
    if request.user.is_authenticated():
        #prof = Profile.objects.get(id=request.user.id)
        #if not prof.nickname_is_set:
        #    return HttpResponseRedirect('/login/set_nickname/?target=/meas/?target='+target)
        response = render_to_response('meas/meas-index.html', { 'target':target },
        context_instance=RequestContext(request))
        response["P3P"] = 'CP="IDC DSP COR ADM DEVi TAIi PSA PSD IVAi IVDi CONi HIS OUR IND CNT"'
        return response
    else:
        return HttpResponseRedirect('/accounts/login/?next=/meas/?target='+target)

	
		
		
def steps_today(request):
	if request.user.is_authenticated():
	    user = request.user.pk
	    check = steps_check(user)
	    if (check==True):
		now =datetime.now()
		diet_suggestion = DietSuggestion.objects.all()
		lastday= now + timedelta(days=1)
		steps_all = Step.objects.filter(user=request.user.pk,date_time__gt=now.strftime("%Y-%m-%d"),
						date_time__lt=lastday.strftime("%Y-%m-%d"))
		if (steps_all):
			for st in steps_all:  
				steps_array=st.steps.split(',')
				tt=st.total
				calories=st.calories
			avg=[]
			avg_total=0
			for a in steps_array:
				if (int(a)>0):
					avg.append(a)
			for t in avg:
				avg_total += int(t)
			travel_today = "%0.2f" % float(int(tt)/1440.00)
			info = [int(tt), travel_today, "%0.2f" % calories, avg_total/len(avg)]
		else:
			info = [0,'0.00','0.00']
			steps_array = ['0']*24
		time_list =[]
		steps=[]
		for i in range(0,24):
			t=time(i)
			time_list.append(t.strftime('%H:%M'))
			steps.append([steps_array[i],time_list[i]])
		try:
			fb_share = steps_all[0].total	
			fb_share = 'Bugün '+ str(fb_share)+' adım attım.'
		except:
			fb_share = ''		
		user = User.objects.get(id=request.user.id)
		badge_to_user = BadgeToUser.objects.filter(user=user)
		hourly_step_avg_int = None
		hourly_step_avg = HourlyStepAvg.objects.filter(user=user)
		if len(hourly_step_avg) > 0:
			hourly_step_avg_list = hourly_step_avg[0].steps.split(',')
			hourly_step_avg_int = [0]*24
			for itr in range(0,24):
				hourly_step_avg_int[itr] = int(hourly_step_avg_list[itr])
		response = render_to_response('meas/steps.html', { 'steps': steps ,
														   'user':user,
														   'badge_to_user':badge_to_user,
														   'hourly_step_avg_int':hourly_step_avg_int,
														   'total':steps_all, 
														   'diet':diet_suggestion, 
														   'info':info,
														   'show_ads':settings.SHOW_ADS_MEAS,
														   'fb_share':fb_share } ,
		context_instance=RequestContext(request))
		response["P3P"] = 'CP="IDC DSP COR ADM DEVi TAIi PSA PSD IVAi IVDi CONi HIS OUR IND CNT"'
		return response
	    else:
		redirect_url = 'http://'+ settings.DOMAIN_NAME +'/meas/mobil/'
		redirect_code = """
		<script type="text/javascript">
		window.location.href='%s';
		</script>
		""" % redirect_url;
		return HttpResponse(redirect_code,mimetype="text/html")
	else:
		redirect_url = 'http://'+ settings.DOMAIN_NAME +'/accounts/login?next=/meas/fbapp/'
		redirect_code = """
		<meta http-equiv="P3P" content='CP="IDC DSP COR CURa ADMa OUR IND PHY ONL COM STA"'>
		<script type="text/javascript">
		top.location.href='%s';
		</script>
		""" % redirect_url;
		return HttpResponse(redirect_code,mimetype="text/html")

def points(request):
	if request.user.is_authenticated():
			profile = Profile.objects.get(user=request.user)
			#if profile.nickname_is_set:
			#	redirect_url = 'http://'+ settings.DOMAIN_NAME +'/accounts/set_nickname/?next=/meas/points/'
			#	redirect_code = ""
			#	return HttpResponse(redirect_code,mimetype="text/html")
			user = User.objects.get(id=request.user.id)
			prof,created = UserScore.objects.get_or_create(user=user)
			xpoints = prof.xscore
			current_points = prof.score
			top_points = prof.high_score
			last_week_points = prof.last_week_score
			near_20 = []
			rank_pos = 6
			for i in range(5,0,-1):
				try:
					u = UserScore.objects.get(score_rank=prof.score_rank-i)
					near_20.append(u)
				except Exception,err:
					continue
			for i in range(0,6):
				try:
					if i==0:
						rank_pos = len(near_20)
					u = UserScore.objects.get(score_rank=prof.score_rank+i)
					near_20.append(u)
				except Exception,err:
					continue
			now = datetime.now()
			point_list=[]
			date_list=[]
			point_date_list=[]
			total_point = 0
			last_monday = now - timedelta(days=now.weekday())
			for day in range(0,7):
				that_day = last_monday + timedelta(days=day)
				date_list.append(that_day)
				a = that_day
				points = Point.objects.filter(user=user, action_date__year=that_day.year, 
					action_date__month=that_day.month, action_date__day=that_day.day)
				if points.count() > 0:
						for point in points:
							total_point += int(point.points_earned)
						point_list.append(str(total_point))
						b = point.points_earned
				else:
						point_list.append(str(0))
						b = 0
				point_date_list.append([a,b]) 
			help_content = Content.objects.get(page="point_help")
			point_history = None
			points = Point.objects.filter(user=user).order_by('-action_date')
			return render_to_response('meas/points.html', {
														   'current_points':current_points, 
														   'last_week_points':last_week_points, 
														   'top_points':last_week_points, 
														   'xpoints':xpoints, 
														   'rank_pos':rank_pos, 
														   'help_content':help_content, 
														   'points':points, 
														   'point_date_list':point_date_list, 
														   'top_25':near_20 }, 
														   context_instance=RequestContext(request))
	else:
			#TODO reverse...
			return HttpResponsePermanentRedirect('/accounts/login?next=/meas/steps/')

def steps_monthly(request):
	if request.user.is_authenticated():
			now =datetime.now()
			diet_suggestion = DietSuggestion.objects.all()
			day = 30 
			last_month = now - timedelta(days=day)
			now_plus = now + timedelta(days=1)
			steps_all = Step.objects.filter(user=request.user.pk,
												date_time__gt=last_month.strftime("%Y-%m-%d"),
												date_time__lt=now_plus.strftime("%Y-%m-%d"))
			total_list=[]
			total = 0
			calories = 0
			for st in steps_all:
				total_list.append(st.total)
				total +=int(st.total)
				calories +=float(st.calories)
			date_list=[]
			total_list.reverse()
			steps_monthly_list=[]
			avg=0
			for i in range(0,30):
				date_list.append(now - timedelta(days=int(i)+1))
				a = date_list[i]
				try:
					b = total_list[i]
					avg += int(b)
					avg_r=avg/len(total_list)
					fb_share = 'Bu ay '+str(total)+' adım attım.'
				except:
					b= 0
					avg_r = 0
					fb_share = ''
				steps_monthly_list.append([a,b])
			travel_month = "%0.2f" % float(total/1440.00)		
			info = [int(total), travel_month, "%0.2f" % calories, avg_r]
			return render_to_response('meas/total.html', { 'steps': steps_monthly_list,
														   'total':total, 
														   'diet':diet_suggestion, 
														   'info':info,
														   'fb_share':fb_share,	}, 
														   context_instance=RequestContext(request))
	else:
			#TODO reverse...
			return HttpResponsePermanentRedirect('/accounts/login?next=/meas/steps/')


def calories(request):
	if request.user.is_authenticated():
			now =datetime.now()
			calories_suggestion = CaloriesSuggestion.objects.order_by('?')[:2]
			day = 30 
			last_month = now - timedelta(days=day)
			now_plus = now + timedelta(days=1)
			steps_all = Step.objects.filter(user=request.user.pk,
																			date_time__gt=last_month.strftime("%Y-%m-%d"),
																			date_time__lt=now_plus.strftime("%Y-%m-%d"))
			calories_list=[]
			total = 0
			calories_total = 0
			for st in steps_all:
				calories_list.append(str(st.calories))
				calories_total +=float(st.calories)
				total +=int(st.total)
			date_list=[]
			steps_monthly_list=[]
			counter = 0
			for i in range(0,30):
				date_list.append(now - timedelta(days=int(i)+1))
				a = date_list[i]
				try:
					b=calories_list[i]
					counter+=1
					calories_avg = float(calories_total)/counter
					fb_share = 'Bu ay '+calories_total+' kalori harcadım.'
				except:
					b='0'
					calories_avg = 0
					fb_share = ''
				steps_monthly_list.append([a,b])
			travel_month = "%0.2f" % float(total/1440.00)
			calories_avg_int = int(calories_avg)	
			calories_avg = "%0.2f" % calories_avg		
			calories_total = "%0.2f" % calories_total
			info = [total, travel_month, calories_total, calories_avg, calories_avg_int]
			return render_to_response('meas/calorie.html', { 'steps': steps_monthly_list,
															 'total':total, 
                                                             'suggestion':calories_suggestion, 
                                                             'info':info,
															 'fb_share':fb_share}, 
                                                             context_instance=RequestContext(request))
	else:
			#TODO reverse...
			return HttpResponsePermanentRedirect('/accounts/login?next=/meas/steps/')




def grand_total_steps(request):
	if request.method == 'POST':
		response_data={"True": cache.get('grand_steps')}
		return HttpResponse(json.dumps(response_data), mimetype="application/json")
	else:
		return HttpResponse('Fail')

def try_function(request):
	#if cache.get('grand_steps'):
	#	return HttpResponse(cache.get('grand_steps'))
	#else:
	return HttpResponse(cache.get('grand_steps'))

def calories_convert(request):
	steps_all=Step.objects.all()
	for m in steps_all:
		steps = Step.objects.get(id=m.id)
		new_calories=(steps.calories/2.02)*0.05
		new_calories="%0.2f" % new_calories
		update_cal=Step.objects.filter(id=m.id)
		update_cal.update(calories=new_calories)
	return HttpResponse('ok')

def meas_support(request):
	try:
		if request.method == 'POST':
			email = request.POST.get('email', '') 
			#return HttpResponse(email)
			html_content = render_to_string('meas/support_email.html') 
			text_content = strip_tags(html_content)
			subject, from_email, to = 'Adımsayar Uygulaması', 'adimsayarbilgi@gmail.com', email
			msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
			msg.attach_alternative(html_content, "text/html")
			msg.send()
			return render_to_response('meas/email_send_ok.html')
		else:
			return render_to_response('meas/email_send_ok.html',{'hata':hata})
	except:
		hata=True
		return render_to_response('meas/email_send_ok.html',{'hata':hata})

def bmi(request):
	new_height = request.GET.get('height','')
	new_weight = request.GET.get('weight','')
	new_age = request.GET.get('age','')
	smile=1
	if (new_height) and (new_height) and (new_age):
		profile_up = Profile.objects.filter(user=request.user)
		profile_up.update(
		height = new_height,
		weight = new_weight,
		age = new_age
		)
	try:
		profile = Profile.objects.get(user=request.user)
		age = profile.age
	except:
		profile = None
	if (age <=24 ):
		bmi_advice = 22
	elif (25 <= age <=34):
		bmi_advice = 23
	elif (35 <= age <=44):
		bmi_advice = 23
	elif (45 <= age <=54):
		bmi_advice = 24
	elif (55 <= age <=65):
		bmi_advice = 25
	else:
		bmi_advice = 26

	if (profile.height!=None and profile.weight!=None):
		height,weight = float(profile.height),float(profile.weight)
		bmi = weight/((height/100)*(height/100))
		weight_advice = int(bmi_advice *((height/100)*(height/100)))
		smile_range=int(bmi)
		if ( 20 <= smile_range <= 25):
			smile = 2
		else:
			smile = 4
		bmi = "%0.2f" % bmi
		fb_share = 'Şu an '+str(profile.weight)+' kilodayım.'
	else:
		bmi=1
		weight_advice=None
		fb_share = "Adımsayar'ı kullanarak kilo vermeye başladım."
	content = Content.objects.get(page="bmi_warning")

	return render_to_response('meas/weight.html',{'profile':profile,
												  'bmi':bmi,
                                                  'weight_advice':weight_advice,
												  'content':content,
												  'fb_share':fb_share,
												  'smile':smile},
												  context_instance=RequestContext(request))

def weight(request):
    if request.user.is_authenticated():
        user = User.objects.get(id=request.user.id)
        msg = None
        if request.method == "POST":
            weight_goal = request.POST.get('weight_goal', None)
            weight_goal_duration = request.POST.get('weight_goal_duration', None)
            if weight_goal and weight_goal_duration:
                weight_goal=weight_goal.replace(',','.')
                body_infos = (BodyInfo.objects.filter(user=user)
                    .order_by('date_time').update(weight_goal=float(weight_goal), 
                                  weight_goal_duration=int(weight_goal_duration)))
                msg = "Kaydedildi, grafik guncellendi"
            else:
                weight = request.POST.get("weight", None)
                height = request.POST.get("height", None)
                age = request.POST.get("age", None)
                if (weight) and (height) and (age):
                    body_info = BodyInfo(user=user, age=int(age), 
                        weight=int(weight), height=int(height),gender="F", 
                        weight_float=float(weight))
                    body_info.save()
                    msg = "Kayıt Başarılı"
                else:
                    msg = "Hata: Lütfen Boy, Kilo ve yaş değerlerinizi girin."

        body_infos = BodyInfo.objects.filter(user=user).order_by('date_time')
        fb_share = "Adımsayar'ı kullanarak kilo vermeye başladım."
        content = Content.objects.get(page="bmi_warning")
        return render_to_response('meas/weight2.html',{
                                          'body_infos': body_infos,
                                          'content':content,
                                          'msg':msg,
                                          'fb_share':fb_share},
                                           context_instance=RequestContext(request))


def bmi_image(request):
	weight = request.GET.get('weight','')
	height = request.GET.get('height','')
	chart_hg = request.GET.get('chart_hg','')
	chart_wd = request.GET.get('chart_wd','')
	if not (chart_hg):
		chart_hg = 0
	weight,height,chart_wd,chart_hg = int(weight),int(height),int(chart_wd),int(chart_hg)
	chart = bmi_chart(weight,height,chart_wd,chart_hg)
	response = HttpResponse(mimetype="image/png")
	chart.save(response, 'JPEG',quality=90)
	return response

	
def bmi_chart(weight,height,chart_wd,chart_hg):
    chart_bg = Image.open(settings.MEDIA_ROOT+'/images/bmi_bg.png')
    chart = Image.open(settings.MEDIA_ROOT+'/images/bmi_chart.png')
    point = Image.open(settings.MEDIA_ROOT+"/images/bmi_imge.png")
    chart_x , chart_y = chart.size
    x = float((chart_x/60.0)*(height-150))
    y = float((chart_y/90.0)*(130-weight))
    point_position = int(x)-30, int(y)-60
    chart.paste(point, point_position, point)
    buffer = StringIO.StringIO()
    chart.save(buffer, 'JPEG')
    chart_new = chart
    chart_position = 93,6
    chart_bg.paste(chart_new, chart_position, chart_new )
    if not (chart_hg):
		chart_wd = int(chart_wd*0.78)
		chart_hg = float(chart_wd)*0.45
		chart_hg = int(chart_hg)
    chart_bg = chart_bg.resize((chart_wd, chart_hg),Image.ANTIALIAS)
    return chart_bg
	
def post_feed(request):
	fb = UserAssociation.objects.get(user=request.user.pk)
	access_token = fb.token
	fb_id = fb.identifier
	message = 'www.doktorsensin.com “Doktora Sor” uygulamasını kullanarak sorumu uzmanlara sordum.  \
		Sen de sağlığın hakkında merak ettiğin her şeyi uzman doktorlara ücretsiz olarak sorabilirsin!'
	name = "Doktora Sor uygulaması"
	caption = 'Doktora Sor” bir www.doktorsensin.com uygulamasıdır.'
	description = 'Her biri alanında uzman ve deneyimli 3000’den fazla doktor dilediğiniz branşta \
		soracağınız soruları yanıtlamayı bekliyor! \
		Siz de uygulamayı kullanın sağlığınız için sorun, öğrenin!'
	link = 'https://www.facebook.com/connect/uiserver.php?app_id='+ settings.FACEBOOK_APP_ID +'&method=permissions.request&display=page&next=http%3A%2F%2Ffbserver.acibadem.com.tr%2Finstall&response_type=code&fbconnect=1&perms=email%2Cuser_birthday%2Coffline_access%2Cpublish_stream%2Cuser_location#'
	picture = 'http://fbserver.acibadem.com.tr/site_media/image/post_icon.png'
	tmp = urllib.urlopen("https://graph.facebook.com/"+ fb_id +"/feed?",
		urllib.urlencode(dict(access_token=access_token,
			message=message, link=link, picture=picture,caption=caption,
			name = name, description=description)))
	profile = json.load(tmp)
	return HttpResponse(profile)

def check(request):
	fb = UserAssociation.objects.get(user=2)
	access_token = fb.token
	tmp = urllib.urlopen("https://graph.facebook.com/me?" + 
						    urllib.urlencode(dict(access_token=access_token)))
	profile = json.load(tmp)
	return HttpResponse(profile)

def tracker(request):
	key = request.GET.get('key','')
	if (key):
		id = ((int(key)/8527)-19)/89
		try:
			user = User.objects.get(pk=id)
		except:
			return HttpResponse('Geçersiz Url')
		now =datetime.now()
		lastday= now + timedelta(days=1)
		steps_today = Step.objects.filter(user=user,date_time__gt=now.strftime("%Y-%m-%d"),
						date_time__lt=lastday.strftime("%Y-%m-%d"))
		try:				
			steps_total = steps_today[0].total
		except:
			steps_total = 0
		tracker_background = Image.open(settings.MEDIA_ROOT+'/images/trackers_bg.png')
		tracker_bg_draw = ImageDraw.Draw(tracker_background)
		fontPath = settings.MEDIA_ROOT+'/fonts/digit.ttf'
		font = ImageFont.truetype(fontPath, 26)
		color = (255,255,255) 
		x_axis, y_axis = tracker_background.size
		text=str(steps_total)
		text_x=98 - len(text)*10
		text_pos=(text_x,20)
		tracker_bg_draw.text(text_pos, text, fill=color, font=font)
		del tracker_bg_draw
		slider_pos = 3,2
		if (steps_total >= 10000):
			tracker_smiley_1 = Image.open(settings.MEDIA_ROOT+'/images/smile1_small.png')
			tracker_background.paste(tracker_smiley_1, slider_pos , tracker_smiley_1)
		elif (steps_total >= 7000):
			tracker_smiley_2 = Image.open(settings.MEDIA_ROOT+'/images/smile2_small.png')
			tracker_background.paste(tracker_smiley_2, slider_pos , tracker_smiley_2)
		elif (steps_total >= 4000):
			tracker_smiley_3 = Image.open(settings.MEDIA_ROOT+'/images/smile3_small.png')
			tracker_background.paste(tracker_smiley_3, slider_pos , tracker_smiley_3)
		elif (steps_total >= 1000):
			tracker_smiley_4 = Image.open(settings.MEDIA_ROOT+'/images/smile4_small.png')
			tracker_background.paste(tracker_smiley_4, slider_pos , tracker_smiley_4)
		else:
			tracker_smiley_5 = Image.open(settings.MEDIA_ROOT+'/images/smile5_small.png')
			tracker_background.paste(tracker_smiley_5, slider_pos , tracker_smiley_5)

		response = HttpResponse(mimetype="image/png")
		tracker_background.save(response, 'PNG')
		return response 

	else:
		if request.user.is_authenticated():
			id=request.user.pk
			key = ((id*89)+19)*8527
			url = '/meas/tracker/?key='+str(key)
			return HttpResponseRedirect(url)
		else:
			return HttpResponse("not authenticated")


def pil_image(request):
    initial = request.GET.get('initial', '')
    current = request.GET.get('current', '')
    goal = request.GET.get('goal', '')
    return draw_ticker(0,0, int(initial), int(current), int(goal))

def pil_share(request):
    initial = request.GET.get('initial', '')
    current = request.GET.get('current', '')
    goal = request.GET.get('goal', '')
    image = draw_ticker(0,0, int(initial), int(current), int(goal))
    return render_to_response('tracker/image_share.html', {'image' : image})
	
	
def draw_ticker(background, ticker, x1, xa, x2):
    import Image, ImageDraw, ImageFont 
    fontPath = settings.MEDIA_ROOT+'/trac_images/digit.ttf'
    font = ImageFont.truetype(fontPath, 18)
    im_background = Image.open(settings.MEDIA_ROOT+'/trac_images/bar281.png')
    im_slider = Image.open(settings.MEDIA_ROOT+"/trac_images/heart.png")
    draw = ImageDraw.Draw(im_background)   # create a drawing object that is
    red = (255,0,0)    # color of our text
    x_axis, y_axis = im_background.size
    x_incr = x_axis / 11;
    x_pos = 5;    
    val_incr = (x1 - x2) / 9
    val = x1;
    for i in range(1,12):
	text_pos = (x_pos,55) # top-left position of our text
	if (i == 1):
	    text = str(x1)
	elif (i == 11):
	    text = str(x2)
	else:
	    text = str(val) # text to draw
	draw.text(text_pos, text, fill=red, font=font)
	x_pos += x_incr+1
	val -= val_incr
    del draw # I'm done drawing so I don't need this anymore
    slider_pos_x = float( ( ((x1) / (xa * 1.0001 )) - 1 )* x_axis )
    #return HttpResponse(pos)
    slider_pos = slider_pos_x,10
    im_background.paste(im_slider, slider_pos,im_slider)
    response = HttpResponse(mimetype="image/png")
    im_background.save(response, 'PNG')
    return response # and we're done!

def get_weekly_steps(email):
	user = User.objects.get(email=email)
	now =datetime.now()
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
	return "OK", step_list, total_steps, calories

def users_top(request):
    top_25 = Profile.objects.all().order_by('-point')[:25]
    response = render_to_response('users_top.html',{'top_25':top_25}, context_instance=RequestContext(request))
    response["P3P"] = 'CP="IDC DSP COR ADM DEVi TAIi PSA PSD IVAi IVDi CONi HIS OUR IND CNT"'
    return response


def user_point_cal():
    import decimal
    users = User.objects.all()
    for user in users:
        try:
            profile = Profile.objects.get(user=user)
            user_steps = Step.objects.filter(user=user)
            user_total_step = 0
            for step in user_steps:
                user_total_step += step.total
            profile.total_step = user_total_step
            profile.point = decimal.Decimal(str(user_total_step * 0.002)).quantize(decimal.Decimal("0.1"), rounding=decimal.ROUND_HALF_EVEN)
            profile.save()
            print profile.total_step
            print profile.point
        except Exception:
            pass
    return 'ok'
