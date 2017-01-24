# -*- coding: utf-8 -*-
from poll.models import Answer,Question
from django.shortcuts import render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from django.template.context import RequestContext
from django.conf import settings
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from poll.models import Question, Answer, UserAnswer
from content.models import Content
from mailing.functions import check_validator
import md5
import hashlib


def poll_widget(request):
    question = Question.objects.order_by('?')[0]
    answers = Answer.objects.filter(question=question)
    return render_to_response('poll/question_widget.html',{'question':question,'answers':answers},
                                context_instance=RequestContext(request))

def answer(request):
    answer_id = request.POST.get('answer','')
    answer = Answer.objects.get(pk=answer_id)
    count = answer.count + 1
    answer.count = count
    answer.save()
    return HttpResponse('ok')

def poll_result(request, poll_id):
    if check_validator(request):
        try:
            answer_id = request.GET.get('answer',None)
            user_id = request.GET.get('key_id',None)
            user = User.objects.get(id=long(user_id))
            question = Question.objects.get(id=long(poll_id))
            answer = Answer.objects.get(id=long(answer_id))
            answer.count += 1
            answer.save()
            user_answer = UserAnswer(user=user, question=question, answer=answer)
            user_answer.save()
            return HttpResponseRedirect(reverse(poll_result,args=[poll_id])) 
        except Exception, err:
            pass
    question = Question.objects.get(id=poll_id)
    answers = Answer.objects.filter(question=question)
    content = Content.objects.filter(page="question_"+str(poll_id))[0]
    return render_to_response('poll/result.html',{'question':question,'answers':answers, 
                          'content':content}, context_instance=RequestContext(request))

def poll_question(request, poll_id):
    question = Question.objects.get(id=poll_id)
    answers = Answer.objects.filter(question=question)
    return render_to_response('poll/question.html',{'question':question,'answers':answers},
                                context_instance=RequestContext(request))
