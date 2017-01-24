from django.contrib import admin 
from poll.models import Question,Answer,UserAnswer

class QuestionInline(admin.TabularInline):
    model = Answer
    extra = 6
    exclude = ['count']


class QuestionAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Question._meta.fields if f.name != 'id']
    inlines = [QuestionInline]

class AnswerAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Answer._meta.fields if f.name != 'id']

class UserAnswerAdmin(admin.ModelAdmin):
    list_display = [f.name for f in UserAnswer._meta.fields if f.name != 'id']

admin.site.register(Question,QuestionAdmin)
admin.site.register(Answer,AnswerAdmin)
admin.site.register(UserAnswer,UserAnswerAdmin)

