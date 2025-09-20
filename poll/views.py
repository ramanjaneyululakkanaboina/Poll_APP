from django.shortcuts import render, redirect,get_object_or_404
from .models import Question, Choice
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import Questionform, SignupForm
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    latest_question = Question.objects.filter(is_active=True).order_by('-pub_date')[:5]
    return render(request, 'poll/index.html', {'latest_question': latest_question })

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
    else:
        latest_question = Question.objects.order_by('-pub_date')[:5]
        return render(request, 'poll/view_votes.html', {'latest_question': latest_question })

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