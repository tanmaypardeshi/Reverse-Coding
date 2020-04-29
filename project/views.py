import random
from datetime import datetime, timedelta

from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from .models import Questions, Profile, Response


def signup(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        player1 = request.POST.get('player1')
        mobile1 = request.POST.get('mobile1')
        email1 = request.POST.get('email1')
        player2 = request.POST.get('player2')
        mobile2 = request.POST.get('mobile2')
        if mobile2 == '':
            mobile2 = 9999999999
        email2 = request.POST.get('email2')
        level = int(request.POST.get('level'))
        user = User.objects.create_user(username=username, password=password)
        profile = Profile(user=user, player1=player1, mobile1=mobile1, email1=email1, player2=player2, mobile2=mobile2,
                          email2=email2, level=level)
        profile.save()

        if user is not None:
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('instructions')
        else:
            return render(request, 'project/signup.html')
    else:
        return render(request, 'project/signup.html')


@login_required
def instructions(request):
    if request.method == "POST":
        profile = Profile.objects.get(user=request.user)
        profile.login_time = datetime.now()
        profile.logout_time = profile.login_time + timedelta(minutes=28)
        if profile.level == 0:
            qno = 1
        else:
            qno = 11
        profile.save()
        return redirect('questions', qno)
    else:
        return render(request, 'project/RCIns.html')


@login_required
def generate(request):
    profile = Profile.objects.get(user=request.user)
    while True:
        if profile.attempted < 10:
            if profile.level == 0:
                qno = random.randint(1, 10)
                for i in profile.visited.split(','):
                    if i != str(qno):
                        continue
                    else:
                        return redirect('generate')
                profile.visited = profile.visited + ',' + str(qno)
                profile.current_qno = qno
                profile.save()
                return redirect('questions', qno)
            if profile.level == 1:
                qno = random.randint(11, 20)
                for i in profile.visited.split(','):
                    if i != str(qno):
                        continue
                    else:
                        return redirect('generate')
                profile.visited = profile.visited + ',' + str(qno)
                profile.current_qno = qno
                profile.save()
                return redirect('questions', qno)
        else:
            profile.save()
            return redirect('logout')


@login_required
def questions(request, qno):
    profile = Profile.objects.get(user=request.user)
    profile.current_qno = qno
    cur_time = datetime.now()
    time_remain = (profile.logout_time.hour * 60 * 60) + (
                profile.logout_time.minute * 60) + profile.logout_time.second - \
                  (cur_time.hour * 60 * 60) - (cur_time.minute * 60) - cur_time.second
    if time_remain == 0:
        return redirect('logout')
    profile.save()

    if request.method == "GET":
        question = Questions.objects.get(pk=profile.current_qno)
        context = {'profile': profile, 'question': question, 'your_time': time_remain}
        return render(request, 'project/Codingpage.html', context)

    else:
        question = Questions.objects.get(pk=qno)
        if profile.attempt_counter == 2:
            profile.current_qno = qno
            profile.attempt1 = request.POST.get('attempt1')
            profile.save()
            if profile.attempt1 != '':
                profile.attempt1 = int(profile.attempt1)
                response = Response.objects.create(user=request.user, question=question, attempt1=profile.attempt1)
                response.save()
                if question.answer == profile.attempt1:
                    profile.score = profile.score + profile.increment
                    profile.correct = profile.correct + 1
                    profile.attempted = profile.attempted + 1
                    profile.save()
                    return redirect('generate')
                else:
                    profile.increment = 2
                    profile.decrement = -1
                    profile.attempt_counter = 1
                    profile.save()
                    question = Questions.objects.get(pk=qno)
                    context = {'profile': profile, 'question': question, 'your_time': time_remain,
                               'answer': profile.attempt1}
                    return render(request, 'project/Codingpage.html', context)

            else:
                question = Questions.objects.get(pk=profile.current_qno)
                context = {'profile': profile, 'question': question, 'your_time': time_remain}
                return render(request, 'project/Codingpage.html', context)

        elif profile.attempt_counter == 1:
            attempt2 = request.POST.get('attempt2')
            question = Questions.objects.get(pk=profile.current_qno)
            if attempt2 != '':
                attempt2 = int(attempt2)
                response = Response.objects.create(user=request.user, question=question, attempt2=attempt2)
                response.save()
                if question.answer == attempt2:
                    profile.score = profile.score + profile.increment
                    profile.correct = profile.correct + 1
                else:
                    profile.score = profile.score + profile.decrement
                profile.attempt_counter = 2
                profile.attempted = profile.attempted + 1
                profile.increment = 4
                profile.decrement = 0
                profile.save()
                return redirect('generate')
            else:
                question = Questions.objects.get(pk=profile.current_qno)
                context = {'profile': profile, 'question': question, 'your_time': time_remain,
                           'answer': profile.attempt1}
                return render(request, 'project/Codingpage.html', context)


def logout_user(request):
    try:
        profile = Profile.objects.get(user=request.user)
        context = {'profile': profile}
        logout(request)
        return render(request, 'project/Result_page.html', context)
    except:
        return redirect('signup')


def validate_username(request):
    username = request.GET.get('username', None)
    data = {
        'is_taken': User.objects.filter(username__iexact=username).exists()
    }
    return JsonResponse(data)


def emergency(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        password1 = request.POST.get('superpass')
        extra_time = int(request.POST.get('time'))

        if not password1 == "TPPN2019":
            return render(request, 'project/emergency.html', {'error': "Super Password is wrong"})
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                profile = Profile.objects.get(user=request.user)
                profile.logout_time = profile.logout_time + timedelta(seconds=extra_time)
                profile.save()
                question = Questions.objects.get(pk=profile.current_qno, level=profile.level)
                cur_time = datetime.now()
                time_remain = (profile.logout_time.hour * 60 * 60) + (
                        profile.logout_time.minute * 60) + profile.logout_time.second - (cur_time.hour * 60 * 60) - (
                                      cur_time.minute * 60) - cur_time.second
                context = {'profile': profile, 'question': question, 'your_time': time_remain}
                return render(request, 'project/Codingpage.html', context)
        else:
            return render(request, 'project/emergency.html')
    else:
        return render(request, 'project/emergency.html')
