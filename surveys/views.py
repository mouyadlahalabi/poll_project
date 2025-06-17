from django.shortcuts import render, redirect
from .models import Survey, Question, Option
import json
from django.contrib.auth.decorators import login_required
@login_required
def create_survey(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        questions_data = request.POST.getlist('questions[]')

        # إنشاء الاستبيان
        survey = Survey.objects.create(
            title=title,
            description=description,
            created_by=request.user
        )

        # إنشاء الأسئلة
        for question_json in questions_data:
            question_info = json.loads(question_json)
            text = question_info['text']
            qtype = question_info['type']
            options = question_info.get('options', [])

            question = Question.objects.create(
                survey=survey,
                text=text,
                question_type=qtype
            )

            if qtype in ['multiple', 'single']:
                for option_text in options:
                    Option.objects.create(
                        question=question,
                        text=option_text
                    )

        # استرجاع كل الأسئلة المرتبطة بالاستبيان مع الخيارات
        questions = survey.questions.prefetch_related('options')


        return render(request, 'surveys/success.html', {
            'survey': survey,
            'questions': questions,
        })

    return render(request, 'surveys/survey_form.html')


from django.shortcuts import get_object_or_404, redirect


def edit_survey(request, survey_id):
    survey = get_object_or_404(Survey, id=survey_id)
    questions = survey.questions.all()

    if request.method == 'POST':
        # تحديث عنوان ووصف الاستبيان
        survey.title = request.POST.get('title')
        survey.description = request.POST.get('description')
        survey.save()

        # تحديث الأسئلة الحالية
        for question in questions:
            text = request.POST.get(f'question_{question.id}_text')
            q_type = request.POST.get(f'question_{question.id}_type')

            if text:
                question.text = text
                question.question_type = q_type
                question.save()

                # تحديث الخيارات إذا لم يكن نصي
                if q_type != 'text':
                    for idx, option in enumerate(question.options.all(), start=1):
                        option_text = request.POST.get(f'question_{question.id}_option_{idx}')
                        if option_text:
                            option.text = option_text
                            option.save()
            else:
                # حذف السؤال إذا لم يتم إرسال نصه
                question.delete()

        # التعامل مع الأسئلة الجديدة
        new_texts = request.POST.getlist('new_question_text[]')
        new_types = request.POST.getlist('new_question_type[]')

        for i in range(len(new_texts)):
            text = new_texts[i]
            q_type = new_types[i]
            if text.strip():
                new_question = Question.objects.create(
                    survey=survey,
                    text=text,
                    question_type=q_type
                )
                # حفظ الخيارات للأسئلة الجديدة إذا كانت من نوع اختيار
                if q_type != 'text':
                    options = request.POST.getlist(f'new_question_option_{i}[]')
                    for opt_text in options:
                        if opt_text.strip():
                            Option.objects.create(question=new_question, text=opt_text)

        return redirect('surveys:survey_edit_success', survey_id=survey.id)

    return render(request, 'surveys/edit_survey.html', {'survey': survey, 'questions': questions})


def survey_success(request, survey_id):
    survey = Survey.objects.get(id=survey_id)
    return render(request, 'surveys/success.html', {'survey': survey})


from django.shortcuts import render

def survey_edit_success(request, survey_id):
    return render(request, 'surveys/survey_edit_success.html', {'survey_id': survey_id})

@login_required
def list_surveys(request):
    surveys = Survey.objects.filter(created_by=request.user)
    return render(request, 'surveys/list_surveys.html', {'surveys': surveys})

from django.views.decorators.http import require_POST

@require_POST
@login_required
def delete_survey(request, survey_id):
    survey = get_object_or_404(Survey, id=survey_id)
    
    # (اختياري) تأكد أن المستخدم هو من أنشأ الاستبيان
    if survey.created_by != request.user:
        return redirect('surveys:list_surveys')  # أو عرض رسالة خطأ

    survey.delete()
    return redirect('surveys:list_surveys')
    
def info_view(request):
    return render(request, 'surveys/info.html')
def view_survey(request, survey_id):
    survey = get_object_or_404(Survey, pk=survey_id)
    questions = survey.questions.all()

    if request.method == 'POST':
        for question in questions:
            key = f'answer_{question.id}'
            if question.question_type == 'multiple':
                selected_options = request.POST.getlist(key)
            else:
                selected_options = [request.POST.get(key)]

            for opt_text in selected_options:
                try:
                    option = question.options.get(text=opt_text)
                    option.vote_count += 1
                    option.save()
                except Option.DoesNotExist:
                    continue
        return redirect('surveys:view_survey', survey_id=survey.id)

    return render(request, 'surveys/view_survey.html', {
        'survey': survey,
        'questions': questions,
    })




from .models import  Response, Answer

def submit_survey(request, survey_id):
    survey = get_object_or_404(Survey, id=survey_id)
    questions = survey.questions.all()

    if request.method == 'POST':
        # إنشاء كائن Response جديد
        response = Response.objects.create(survey=survey)

        for question in questions:
            field_name = f'answer_{question.id}'
            
            # اجلب الإجابات حسب نوع السؤال
            if question.question_type == 'multiple':
                answers = request.POST.getlist(field_name)
            else:
                answers = [request.POST.get(field_name)]

            # أنشئ كائن Answer لكل إجابة
            for answer_text in answers:
                if answer_text:
                    Answer.objects.create(
                        response=response,
                        question=question,
                        text=answer_text
                    )

        # الرجوع إلى نفس صفحة الاستبيان بعد الحفظ

        return redirect('surveys:view_survey', survey_id=survey.id)

    # إذا لم يكن الطلب POST، أعد تحميل الصفحة
    return redirect('surveys:view_survey', survey_id=survey.id)







from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404, redirect
from .models import Survey

# @staff_member_required  # أو @user_passes_test(lambda u: u.is_superuser)
# def ADdeletesurvey(request, survey_id):
#     survey = get_object_or_404(Survey, id=survey_id)
#     if request.method == 'POST':
#         survey.delete()
#     return redirect('users:admin_dashboard')  # أو الصفحة المناسبة


def ADview_survey(request, survey_id):
    survey = get_object_or_404(Survey, id=survey_id)
    return render(request, 'surveys/ADview_survey.html', {'survey': survey})




