from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from rest_framework import generics

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http.response import HttpResponse

from .models import Books
from accounts.models import *

import json, requests
import re
from django.db.models import Sum, Q, Avg

from .serializer import PostSerializer

def viewbase(request):
    return render(request, 'index.html')

def viewinformation(request):
    return render(request, 'view_information.html')

def viewalgorithm(request):
    return render(request, 'view_algorithm.html')

def viewdata(request):
    return render(request, 'view_data.html')

def viewpurhase(request):
    data = json.loads(request.POST.get('json_items'))
    return redirect('posts:view_algorithm')

# algorithm books
@login_required
def viewparser(request):

    api_request = requests.get('https://api.itbook.store/1.0/search/algorithm')
    print(api_request)
    try:
        api_json = json.loads(api_request.text)
    except Exception as e:
        api_json = "Error"

    api = api_json["books"]

    u_id = request.user.id
    # Profile = userid => pk
    user_data = Profile.objects.filter(Q(user_id=u_id))
    # 해당 pk에 해당하는 객체 하나만
    cartuser = user_data[0]
    # 위의 객체를 view_parser.html에 렌더링

    return render(request, 'view_parser.html', {'api':api, 'cartuser':cartuser})

@csrf_exempt
@login_required
def cart_algorithm(request, user_id):

    user_detail = get_object_or_404(Profile, pk=user_id)

    if request.POST.get('action') == 'post':

        # Receive data from client(input)
        book_id = str(request.POST.get('id'))
        book_title = str(request.POST.get('title'))
        book_subtitle = str(request.POST.get('subtitle'))
        book_isbn13 = str(request.POST.get('isbn13'))
        book_price = str(request.POST.get('price'))
        book_url = str(request.POST.get('url'))

        cleaned_price = re.findall("\d+.\d+", book_price)[0]
        cleaned_price = float(cleaned_price)
        print(cleaned_price)

        book_genre = 'Algorithm'

    Books.objects.create(title=book_title, subtitle=book_subtitle,
                         isbn13=book_isbn13, price=cleaned_price, url=book_url , genre = book_genre, user = user_detail)

    return redirect('posts:view_parser')

# information book
@login_required
def viewparser2(request):

    api_request = requests.get('https://api.itbook.store/1.0/search/information')
    print(api_request)

    try:
        api_json = json.loads(api_request.text)
    except Exception as e:
        api_json = "Error"

    api = api_json["books"]

    u_id = request.user.id
    # Profile = userid => pk
    user_data = Profile.objects.filter(Q(user_id=u_id))
    # 해당 pk에 해당하는 객체 하나만
    cartuser = user_data[0]
    # 위의 객체를 view_parser.html에 렌더링

    return render(request, 'view_parser2.html', {'api':api, 'cartuser':cartuser})


@csrf_exempt
@login_required
def cart_algorithm2(request, user_id):

    user_detail = get_object_or_404(Profile, pk=user_id)

    if request.POST.get('action') == 'post':

        # Receive data from client(input)
        book_id = str(request.POST.get('id'))
        book_title = str(request.POST.get('title'))
        book_subtitle = str(request.POST.get('subtitle'))
        book_isbn13 = str(request.POST.get('isbn13'))
        book_price = str(request.POST.get('price'))
        book_url = str(request.POST.get('url'))

        cleaned_price = re.findall("\d+.\d+", book_price)[0]
        cleaned_price = float(cleaned_price)

        book_genre = 'Information'
        print(cleaned_price)

    Books.objects.create(title=book_title, subtitle=book_subtitle,
                         isbn13=book_isbn13, price=cleaned_price, url=book_url, genre=book_genre, user=user_detail)

    return redirect('posts:view_parser2')


# data book
@login_required
def viewparser3(request):
    api_request = requests.get('https://api.itbook.store/1.0/search/data')
    print(api_request)
    try:
        api_json = json.loads(api_request.text)
    except Exception as e:
        api_json = "Error"
    api = api_json["books"]
    u_id = request.user.id
    # Profile = userid => pk
    user_data = Profile.objects.filter(Q(user_id=u_id))
    # 해당 pk에 해당하는 객체 하나만
    cartuser = user_data[0]
    # 위의 객체를 view_parser.html에 렌더링

    return render(request, 'view_parser3.html', {'api':api, 'cartuser':cartuser})

@login_required
@csrf_exempt
def cart_algorithm3(request, user_id):

    user_detail = get_object_or_404(Profile, pk=user_id)

    if request.POST.get('action') == 'post':

        # Receive data from client(input)
        book_id = str(request.POST.get('id'))
        book_title = str(request.POST.get('title'))
        book_subtitle = str(request.POST.get('subtitle'))
        book_isbn13 = str(request.POST.get('isbn13'))
        book_price = str(request.POST.get('price'))
        book_url = str(request.POST.get('url'))

        cleaned_price = re.findall("\d+.\d+", book_price)[0]
        cleaned_price = float(cleaned_price)

        book_genre = 'Data'
        print(cleaned_price)

    Books.objects.create(title=book_title, subtitle=book_subtitle,
                         isbn13=book_isbn13, price=cleaned_price, url=book_url, genre=book_genre, user=user_detail)

    return redirect('posts:view_parser3')


@csrf_exempt
@login_required
def cart_view(request):

    # request => get auth user id
    u_id = request.user.id
    # Profile = userid => pk
    user_data = Profile.objects.filter(Q(user_id = u_id))
    # 해당 pk에 해당하는 객체 하나만
    profile = user_data[0]
    # 위의 객체를 view_cart.html에 렌더링

    # Submit prediction and show all
    dataset = Books.objects.all().order_by('-id')
    page = int(request.GET.get('p', 1))
    paginator = Paginator(dataset, 5)
    boards = paginator.get_page(page)
    total = Books.objects.aggregate(Sum('price'))
    print(total)

    return render(request, "view_cart.html", {'dataset':boards, 'total': total, 'profile':profile})

@login_required
@csrf_exempt
def cart_calculate(request):
    profile_instance = Profile.objects.get(user=request.user)
    instance_balance = float(profile_instance.balance)
    if request.POST.get('action') == 'post':

        checkprice = float(request.POST.get('checkprice'))

        if instance_balance >= checkprice :
            instance_balance -= checkprice
            profile_instance.balance = instance_balance
            profile_instance.save()

    return redirect('posts:view_cart')


@csrf_exempt
@login_required
def delete(request, id):
    post = Books.objects.get(id=id)
    post.delete() # 성공 시
    return redirect('posts:view_cart') # 이 부분 redirection

@login_required
def view_piechart(request) :

    username = str(request.user.username)
    data = Books.objects

    genre_data = data.filter(Q(genre__contains= 'Data'))
    genre_information = data.filter(Q(genre__contains= 'Information'))
    genre_algorithm = data.filter(Q(genre__contains= 'Algorithm'))

    data_count = genre_data.count()
    inform_count = genre_information.count()
    algorithm_count = genre_algorithm.count()

    data_avg = genre_data.aggregate(Avg('price'))
    inform_avg = genre_information.aggregate(Avg('price'))
    algorithm_avg = genre_algorithm.aggregate(Avg('price'))

    print(data_avg)

    return render(request, "cart_pie.html", {'data_count':data_count,
                                             'inform_count':inform_count,
                                             'algorithm_count':algorithm_count,
                                             'data_avg':data_avg ,
                                             'inform_avg':inform_avg,
                                             'algorithm_avg':algorithm_avg
                                             })

