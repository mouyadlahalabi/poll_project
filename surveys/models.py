# surveys/models.py

from django.db import models
from django.conf import settings
from django.utils import timezone


class Survey(models.Model):
    title = models.CharField(max_length=255, verbose_name="عنوان الاستبيان")
    description = models.TextField(blank=True, verbose_name="الوصف")
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='surveys',
        verbose_name="أنشئ بواسطة"
    )
    
    created_at = models.DateTimeField(default=timezone.now, verbose_name="تاريخ الإنشاء")


    def __str__(self):
        return self.title

class Question(models.Model):
    QUESTION_TYPES = [
        ('text', 'نصي'),
        ('multiple', 'اختيار متعدد'),
        ('single', 'اختيار وحيد'),
    ]

    survey = models.ForeignKey(Survey, related_name='questions', on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    question_type = models.CharField(max_length=20, choices=QUESTION_TYPES)
    

   

class Option(models.Model):
    question = models.ForeignKey(Question, related_name="options", on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    vote_count = models.PositiveIntegerField(default=0)  # ✅ عدد المرات التي اختير فيها

    def vote_percentage(self):
        total_votes = sum(opt.vote_count for opt in self.question.options.all())
        return (self.vote_count / total_votes) * 100 if total_votes > 0 else 0

class Response(models.Model):
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    submitted_at = models.DateTimeField(auto_now_add=True)

class Answer(models.Model):
    response = models.ForeignKey(Response, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.TextField()


    def __str__(self):
        return self.text
