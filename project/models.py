from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    # Signup
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="Profile")
    player1 = models.CharField(max_length=100)
    email1 = models.EmailField(max_length=100)
    mobile1 = models.IntegerField()
    player2 = models.CharField(max_length=100, default="a", null=True)
    email2 = models.EmailField(max_length=100, default="a@a.com", null=True)
    mobile2 = models.IntegerField(default=999999999, null=True)
    level = models.IntegerField(default=1)

    # Time

    login_time = models.DateTimeField(max_length=100, null=True)
    logout_time = models.DateTimeField(max_length=100, null=True)

    # Score Calculation
    increment = models.IntegerField(default=4)
    decrement = models.IntegerField(default=0)
    current_qno = models.IntegerField(default=1)
    visited = models.CharField(max_length=100, default="")
    attempt_counter = models.IntegerField(default=2)
    score = models.IntegerField(default=0)
    correct = models.IntegerField(default=0)
    attempted = models.IntegerField(default=0)
    attempt1 = models.CharField(default='', max_length=100)

    def __str__(self):
        return self.user.username


class Question(models.Model):
    question = models.TextField(max_length=500, default="")
    answer = models.IntegerField(default=0)
    level = models.IntegerField(default=2)

    def __str__(self):
        return self.question


class Response(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    attempt1 = models.IntegerField(default=0)
    attempt2 = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username + ' - ' + self.question.question
