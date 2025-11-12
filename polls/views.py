from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib import messages
from django.db.models import Count
from django.utils import timezone
from .models import User, Question, Choice, Vote
from .forms import CustomUserCreationForm, UserEditForm, QuestionForm, ChoiceForm


def home(request):
    questions = Question.objects.filter(
        created_at__gte=timezone.now() - timezone.timedelta(hours=24)
    ).exclude(created_at__gt=timezone.now())  # Только не просроченные
    if not request.user.is_staff:
        questions = questions.filter(created_at__gte=timezone.now() - timezone.timedelta(hours=24))
    return render(request, 'polls/home.html', {'questions': questions})


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('polls:home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


def custom_logout_view(request):
    if request.user.is_authenticated:
        logout(request)
        messages.info(request, "Вы успешно вышли из аккаунта.")
    return redirect('polls:home')

@login_required
def profile(request):
    return render(request, 'polls/profile.html', {'user': request.user})

@login_required
def profile_edit(request):
    if request.method == 'POST':
        form = UserEditForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('polls: profile')
    else:
        form = UserEditForm(instance=request.user)
    return render(request, 'polls/profile_edit.html', {'form': form})

@login_required
def delete_profile(request):
    if request.method == 'POST':
        request.user.delete()
        return redirect('polls:home')
    return render(request, 'polls/delete_profile.html')

@login_required
def create_question(request):
    if request.method == 'POST':
        question_form = QuestionForm(request.POST, request.FILES)
        if question_form.is_valid():
            question = question_form.save(commit=False)
            question.author = request.user
            question.save()

            choices_text = request.POST.get('choices', '')
            choices_list = [line.strip() for line in choices_text.splitlines() if line.strip()]
            for text in choices_list:
                Choice.objects.create(question=question, text=text)

            return redirect('polls:home')
    else:
        question_form = QuestionForm()
    return render(request, 'polls/create_question.html', {'form': question_form})

@login_required
def question_detail(request, pk):
    question = get_object_or_404(Question, pk=pk)
    if question.is_expired() and not request.user.is_staff:
        return redirect('home')
    if request.method == 'POST':
        choice_id = request.POST.get('choice')
        if choice_id:
            choice = get_object_or_404(Choice, pk=choice_id, question=question)
            if not Vote.objects.filter(user=request.user, question=question).exists():
                Vote.objects.create(user=request.user, question=question, choice=choice)
                messages.success(request, "Ваш голос учтён!")
            else:
                messages.error(request, "Вы уже голосовали в этом опросе.")
            return redirect('polls:question_detail', pk=pk) # или 'polls:question_detail'

    total_votes = question.vote_set.count()

    choices_with_percent = []
    for choice in question.choices.all():
        votes = choice.vote_set.count()
        percent = (votes / total_votes * 100) if total_votes > 0 else 0
        choices_with_percent.append({
            'choice': choice,
            'votes': votes,
            'percent': round(percent, 1)
        })


    voted = Vote.objects.filter(user=request.user, question=question).exists()

    return render(request, 'polls/question_detail.html', {
        'question': question,
        'choices_with_percent': choices_with_percent,
        'voted': voted,
    })