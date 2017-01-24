from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from core.models import Profile

def username(request, *args, **kwargs):
    if kwargs.get('user'):
        username = kwargs['user'].username
    else:
        username = request.session.get('saved_username')
    return {'username': username}

def redirect_to_form(*args, **kwargs):
    if not kwargs['request'].session.get('saved_username') and \
       kwargs.get('user') is None:
        return HttpResponseRedirect('/login/form/')

def create_profile(request, *args, **kwargs):
    user = User.objects.get(username=kwargs['username'])
    profile, created = Profile.objects.get_or_create(user=user)
    if created:
        profile.save()
