from django.contrib import admin
from .models import *

@admin.action(description='Activate Selected Tickets')
def activate_tickets(modeladmin, request, queryset):
    queryset.update(is_active = True)

@admin.action(description='Deactivate Selected Tickets')
def deactivate_tickets(modeladmin, request, queryset):
    queryset.update(is_active = False)

class QuestionAdmin(admin.ModelAdmin):
    list_display = ("question_text", "pub_date", "is_active")
    search_fields = ["question_text", "pub_date"]
    list_filter = ("pub_date","is_active", "category")
    actions = [activate_tickets, deactivate_tickets]
    
admin.site.register(Question, QuestionAdmin)

class ChoiceAdmin(admin.ModelAdmin):
    list_display = ( "choice_text", "question","votes")
    list_select_related = ('question',)
    list_filter = ["question"]
    search_fields = ["choice_text", "question__question_text"]
admin.site.register(Choice, ChoiceAdmin)

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ("username", "role")
    list_filter = ['role']
    search_fields = ["role"]
admin.site.register(CustomUser, CustomUserAdmin)

admin.site.register(Category)

admin.site.register(Survey)