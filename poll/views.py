from django.shortcuts import render, redirect,get_object_or_404
from .models import *
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import *
from django.utils import timezone
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator

@login_required
def index(request):
    if request.user.role == 'admin':
        latest_question = Question.objects.order_by('-pub_date')[:5]
        return render(request, 'poll/index.html', {'latest_question': latest_question})
    else:
        categories = Category.objects.all()
        return render(request, 'poll/index.html', {'categories': categories})

@login_required
def category_polls(request, category_id):
    """Show all active questions for a specific category."""
    category = get_object_or_404(Category, id=category_id)
    questions = Question.objects.filter(category=category, is_active=True)
    return render(request, 'poll/category_polls.html', {'category': category, 'questions': questions})

@login_required
def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'poll/detail.html', {'question': question})

@login_required
def results(request, question_id):
    question = Question.objects.get(pk=question_id)
    return render(request, 'poll/results.html', {'question': question})

@login_required
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError):
        return render(request, 'poll/detail.html', {
            'question' : question,
            'error_message': "You did not select a choice",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('index'))
    
@login_required
def create_poll(request):
    if request.user.role != 'admin':
        return redirect('index')
    
    else:
        if request.method == 'POST':
            form = Questionform(request.POST)
            num_choices = int(request.POST.get("num_choices"))

            if form.is_valid():
                question = form.save()

                
                for i in range(1, num_choices + 1):
                    choice_text = request.POST.get(f"choice_{i}")
                    if choice_text:
                        Choice.objects.create(question=question, choice_text=choice_text)

                return redirect('index')  
            else:
                return render(request, "poll/create_poll.html", {"question_form": form, 'error_message': "Please correct the errors below and make sure choices are filled.",})
        else:
            form = Questionform()

        return render(request, "poll/create_poll.html", {"question_form": form})
@login_required
def view_votes(request):
    if request.user.role != 'admin':
        return redirect('index')
    
    categories = Category.objects.all()
    selected_category_id = request.GET.get("category")

    # Safe check for category validity
    if selected_category_id and selected_category_id not in ["None", ""]:
        try:
            selected_category_id = int(selected_category_id)
            latest_question = Question.objects.filter(category_id=selected_category_id).order_by('-pub_date')
        except (ValueError, TypeError):
            # If invalid ID or not found, fallback to all questions
            latest_question = Question.objects.order_by('-pub_date')
            selected_category_id = None
    else:
        latest_question = Question.objects.order_by('-pub_date')
        selected_category_id = None

    # Pagination logic
    paginat = Paginator(latest_question, 5)
    page_num = request.GET.get('page')
    page_obj = paginat.get_page(page_num)

    current_page = page_obj.number
    total_pages = paginat.num_pages
    start_page = max(current_page - 1, 1)
    end_page = min(start_page + 2, total_pages)
    if end_page - start_page < 2:
        start_page = max(end_page - 2, 1)
    page_range = range(start_page, end_page + 1)

    context = {
        'latest_question': page_obj,
        'categories': categories,
        'selected_category_id': selected_category_id,
        'page_range': page_range,
    }

    return render(request, 'poll/view_votes.html', context)

def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid(): 
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = SignupForm()
    return render(request, "registration/signup.html", {'form':form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data = request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')                 

@login_required
def create_survey(request):
    if request.user.role != 'admin':
        return redirect('index')

    if request.method == 'POST':
        form = SurveyForm(request.POST)
        if form.is_valid():
            survey = form.save(commit=False)
            survey.created_by = request.user
            survey.start_time = timezone.now()
            survey.save()
            request.session['survey_id'] = survey.id
            return redirect('select_survey_questions')
    else:
        form = SurveyForm()
    
    return render(request, 'poll/create_survey.html', {'form': form})

@login_required
def select_survey_questions(request):
    if request.user.role != 'admin':
        return redirect('index')

    survey_id = request.session.get('survey_id')
    if not survey_id:
        return redirect('create_survey')

    questions = Question.objects.all().select_related('category')

    if request.method == 'POST':
        selected_ids = request.POST.getlist('questions')
        survey = Survey.objects.get(id=survey_id)
        survey.questions.set(selected_ids)
        survey.save()
        return redirect('index')

    return render(request, 'poll/select_survey_questions.html', {'questions': questions})

@login_required
def view_surveys(request):
    surveys = Survey.objects.filter(end_time__gt=timezone.now(), is_active=True)
    return render(request, 'poll/view_surveys.html', {'surveys': surveys})

@login_required
def view_survey(request, survey_id):
    # Only admins can view survey details
    if request.user.role != 'admin':
        return redirect('index')

    survey = get_object_or_404(Survey, id=survey_id)
    questions = survey.questions.prefetch_related('choice_set')

    return render(request, 'poll/view_survey.html', {
        'survey': survey,
        'questions': questions
    })

@login_required
def take_survey(request, survey_id):
    # Only students can take survey
    if request.user.role != 'student':
        return redirect('index')

    survey = get_object_or_404(Survey, id=survey_id)
    questions = survey.questions.prefetch_related('choice_set')

    # Check if survey expired
    if survey.end_time < timezone.now():
        if survey.is_active:
            survey.is_active = False
            survey.save()
        return redirect("survey_list") 

    if request.method == "POST":
        for question in questions:
            selected_choice_id = request.POST.get(f"choice_{question.id}")
            if selected_choice_id:
                choice = Choice.objects.get(id=selected_choice_id)
                choice.votes += 1
                choice.save()
        return redirect("index")

    return render(request, "poll/take_survey.html", {
        "survey": survey,
        "questions": questions,
    })

@login_required
def survey_list(request):
    # Only students can see survey list
    if request.user.role != 'student':
        return redirect('index')

    now = timezone.now()
    for survey in Survey.objects.filter(is_active = True):
        survey.check_expiry()

    active_surveys = Survey.objects.filter(is_active=True).order_by('-start_time')

    return render(request, 'poll/survey_list.html', {
        'active_surveys': active_surveys,
        
    })

@login_required
def view_survey_list(request):
    # Only admin can see survey list
    if request.user.role != 'admin':
        return redirect('index')

    now = timezone.now()
    for survey in Survey.objects.filter(is_active = True):
        survey.check_expiry()

    active_surveys = Survey.objects.filter(is_active=True).order_by('-start_time')
    expired_surveys = Survey.objects.filter(is_active=False).order_by('-end_time')

    return render(request, 'poll/view_survey_list.html', {
        'active_surveys': active_surveys,
        'expired_surveys': expired_surveys,
    })