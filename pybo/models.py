from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Category(models.Model):
    boardCode = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    has_answer = models.BooleanField(default=True)

    def __str__(self):
        return self.boardCode

    def get_absolute_url(self):
        return reverse('pybo:index', args=[self.boardCode])


class Question(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_question')
    subject = models.CharField(max_length=200)
    content = models.TextField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)
    voter = models.ManyToManyField(User, related_name='voter_question')
    view_count = models.IntegerField(null=False, blank=True, default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category_question')

    def __str__(self):
        return self.subject

    def get_absolute_url(self):
        return reverse('pybo:question_detail', args=[self.id])


class Answer(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_answer')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    content = models.TextField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)
    voter = models.ManyToManyField(User, related_name='voter_answer')


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)
    question = models.ForeignKey(Question, null=True, blank=True, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, null=True, blank=True, on_delete=models.CASCADE)


class QuestionCount(models.Model):
    ip = models.CharField(max_length=30)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    def __unicode__(self):
        return self.ip
