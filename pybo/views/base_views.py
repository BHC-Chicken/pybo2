from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.shortcuts import render, get_object_or_404

from ..models import Question, Answer, QuestionCount, Category


def index(request, category_boardCode='qna'):
    page = request.GET.get('page', '1')
    kw = request.GET.get('kw', '')
    so = request.GET.get('so', 'recent')

    category_list = Category.objects.all()
    category = get_object_or_404(Category, boardCode=category_boardCode)

    if so == 'recommend':
        question_list = Question.objects.annotate(num_voter=Count('voter')).order_by('-num_voter', '-create_date') \
            .filter(category=category)
    elif so == 'popular':
        question_list = Question.objects.annotate(num_answer=Count('answer')).order_by('-num_answer', '-create_date') \
            .filter(category=category)
    else:
        question_list = Question.objects.order_by('-create_date').filter(category=category)

    # 검색
    if kw:
        question_list = question_list.filter(
            Q(subject__icontains=kw) |
            Q(content__icontains=kw) |
            Q(author__username__icontains=kw) |
            Q(answer__author__username__icontains=kw)
        ).distinct()

    paginator = Paginator(question_list, 10)
    page_obj = paginator.get_page(page)

    context = {'question_list': page_obj, 'page': page, 'kw': kw, 'so': so,
               'category_list': category_list, 'category': category}
    return render(request, 'pybo/question_list.html', context)


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def detail(request, question_id):
    page = request.GET.get('page', '1')
    so = request.GET.get('so', 'recent')
    question = get_object_or_404(Question, pk=question_id)

    if so == 'recommend':
        answer_list = Answer.objects.annotate(num_voter=Count('voter')).order_by('-num_voter', '-create_date') \
            .filter(question=question)
    else:
        answer_list = Answer.objects.order_by('-create_date').filter(question=question)

    paginator = Paginator(answer_list, 10)
    page_obj = paginator.get_page(page)

    ip = get_client_ip(request)
    cnt = QuestionCount.objects.filter(ip=ip, question=question).count()
    if cnt == 0:
        qc = QuestionCount(ip=ip, question=question)
        qc.save()
        if question.view_count:
            question.view_count += 1
        else:
            question.view_count = 1
        question.save()

    context = {'question': question, 'answer_list': page_obj, 'page': page, 'so': so, 'category': question.category}
    return render(request, 'pybo/question_detail.html', context)
