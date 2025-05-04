# Create your models here.
import datetime

from django.db import models
from django.utils import timezone
from django.contrib import admin #important for admin interface styling


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")

    def __str__(self):
        return self.question_text
    
    #@admin.display() decorator is used to customize the display of the method in the admin interface.
    #boolean=True tells the admin to display the result as a checkmark (✔/✖) instead of True/False.
    #ordering='pub_date' allows the admin list view to sort rows based on the pub_date 
    #   field whensorting by was_published_recently.
    #It also adds a nice label (defaults to the method name, 
    #   but you can override it with description="..." if desired).
    @admin.display(boolean=True, ordering="pub_date", description="Published recently?")
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)
    
class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text
