# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from score.models import Point, UserScore
from django.contrib.auth.models import User
from django.http import HttpResponse
import json

def get_daily_total_points(user, date_time):
    yesterday = (datetime.today() - timedelta(1))
    points = Points.objects.filter(user=user, date_time=date_time)
    total = 0
    for p in points:
        total += p.points_earned
    return total


def get_user_ranking(user):
    rank = None
    try:
        rank = UserScore.objects.get(user=user)
        result = rank.rank
    except Exception, err:
        result = UserScore.objects.all().count()+1
    return result


def get_near_20(request):
    email = "admin@admin.com"
    user = User.objects.get(email=email)
    score = UserScore.objects.get(user=user)
    near_20 = dict()
    rank_pos = 10
    for i in range(10,0,-1):
        try:
            u = UserScore.objects.get(score_rank=score.score_rank-i)
            rank = dict()
            rank['icon'] = ""
            rank['rank'] = u.score_rank
            rank['nickname'] = u.user.username
            rank['score'] = u.score
            near_20[10-i] = rank
        except Exception,err:
            continue
    for i in range(0,10):
        try:
            if i==0:
                rank_pos = len(near_20)
            u = UserScore.objects.get(score_rank=score.score_rank+i)
            rank = dict()
            rank['icon'] = ""
            rank['rank'] = u.score_rank
            rank['nickname'] = u.user.username
            rank['score'] = u.score
            near_20[10+i] = rank
        except Exception,err:
            continue

    json_data = json.dumps(near_20)
    return HttpResponse(json_data, mimetype="application/json")

