from django import forms
from .models import Survey, Question, Option

class SurveyForm(forms.ModelForm):
    class Meta:
        model = Survey
        fields = ['title', 'description']

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['text', 'question_type', 'required', 'order']

OptionFormSet = forms.inlineformset_factory(
    Question, Option, fields=('text',), extra=1, can_delete=True
)