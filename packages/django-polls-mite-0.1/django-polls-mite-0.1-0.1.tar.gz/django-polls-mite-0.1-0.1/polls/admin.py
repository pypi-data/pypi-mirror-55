"""
admin models
"""
from django.contrib import admin

from .models import Question, Choice
# Register your models here.


class ChoiceAdmin(admin.ModelAdmin):
    """
    how model Choice looks in the admin page
    """
    fields = ['choice_text', 'votes']
    readonly_fields = ['votes']


class ChoiceInline(admin.TabularInline):
    """
    tabular representation of Choice inside Question model
    """
    model = Choice
    extra = 3
    fields = ChoiceAdmin.fields
    readonly_fields = ChoiceAdmin.readonly_fields


class QuestionAdmin(admin.ModelAdmin):
    """
    how model Question looks in the admin page
    """
    fieldsets = [
        (None, {'fields': ['question_text']}),
        ('Date Information', {'fields': ['pub_date'], 'classes': ['collapse']})
    ]
    inlines = [ChoiceInline]
    list_display = ('question_text', 'pub_date', 'was_published_recently')
    list_filter = ['pub_date']
    search_fields = ['question_text']
    list_per_page = 10


admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice, ChoiceAdmin)
