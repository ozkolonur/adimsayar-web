from django.db import models
from django.contrib.auth.models import User

ANSWER_CHOICE = (
    (0,'Radio Button'),
    (1,'CheckBox')
)

class Question(models.Model):
    question = models.TextField(max_length=255)
    answer_type = models.IntegerField(default=0,choices=ANSWER_CHOICE)
    def __unicode__(self):
        return self.question

class Answer(models.Model):
    question = models.ForeignKey(Question)
    answer = models.CharField(max_length=255)
    count = models.PositiveIntegerField(default=0)
    def __unicode__(self):
        return self.answer

class UserAnswer(models.Model):
    user = models.ForeignKey(User)
    question = models.ForeignKey(Question)
    answer = models.ForeignKey(Answer)
    date_time = models.DateTimeField(auto_now_add = True)
    def __unicode__(self):
        return u'%s' % self.date_time

