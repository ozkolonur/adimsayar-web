# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from contact.models import Contact
from content.models import Content
from django.template import RequestContext, Context
from django.core.mail import send_mail, BadHeaderError
from django.utils.html import mark_safe
from django.template.loader import render_to_string


def contactview(request):
    name = request.POST.get('name', '')
    subject = request.POST.get('topic', '')
    message = request.POST.get('message', '')
    from_email = request.POST.get('email', '')
    system_email = 'adimsayarbilgi@gmail.com'
    hata = False
    if subject and message and from_email:
        contact = Contact.objects.create(name=name,
                                         subject = subject,
                                         from_email = from_email,
                                         system_email = system_email,
                                         message = message,
                                        )
        try:
            contact.save()
            auto_msg = Content.objects.filter(page="contact_auto_reply_message")
            if auto_msg:
                #message = render_to_string(auto_msg[0].text) sonra düzelticem
                send_mail(auto_msg[0].title, auto_msg[0].text, system_email, (from_email,))
                contact.auto_replied = True
                contact.save()
            else:
                contact.send_error = False
                contact.error_email = from_email
                contact.save()
        except:
            hata = True
        try:
            message = ('Name: '+name + "\n" + 'Email: '+ 
                from_email + "\n" + "\n" + 'Message: ' + "\n" +message)
            send_mail(subject, message, system_email, ('ozkolonur@gmail.com',)) # mailin kime gideceği
        except BadHeaderError:
            hata = True

    if not hata and name:
        result = HttpResponseRedirect('/contact/thankyou/')
    else:
        result = render_to_response('contact/contacts.html',
            {'hata':hata},context_instance=RequestContext(request))
    return result

def thankyou(request):
    content = Content.objects.filter(page="contact_thankyou")
    if content:
        content = content[0]
    else:
        content = None
    return render_to_response('contact/thankyou.html', {'content':content},context_instance=RequestContext(request))
