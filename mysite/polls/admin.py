from django.contrib import admin

# Register your models here.
from .models import Choice,Question

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 2 # Number of extra blank choice lines to display

class QuestionAdmin(admin.ModelAdmin):
    # The fields to be used in displaying a particular item the Question model for editing
    fieldsets = [
        ("Identifying Information", {"fields": ["question_text"]}),
        ("Date information", {"fields": ["pub_date"]}),
    ]
    inlines = [ChoiceInline]

    # The fields to be used when listing the data in the Question model
    list_display = ("question_text", "pub_date", "was_published_recently")
    
    list_filter = ["pub_date"]

admin.site.register(Question, QuestionAdmin)