from django.shortcuts import render
from myproject.config_params import char_values, frequency
from .utils import create_grid_of_chars, calculate_winning_points
from django.http import HttpResponse, HttpResponseRedirect
import json
from django.utils.safestring import mark_safe
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from base.models import Account_Information
from datetime import datetime


@login_required
def slot_machine(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/')
    user = request.user
    try:
        account_information_obj = Account_Information.objects.get(user=user)
    except:
        account_information_obj = None
        
    current_month = datetime.now().month
    last_login_month = account_information_obj.user.last_login.month
    if last_login_month!=current_month and account_information_obj:
        account_information_obj.current_month_balance = 5000
        account_information_obj.save()

    grid = [['A','B','D'],['7','#','C'],['~','~','~']]
    return render(request, "base/slot_machine.html", {'grid':grid, 'wins': account_information_obj.no_of_wins,'account_information_obj': account_information_obj})

def home(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/play/')
    return render(request, "base/home.html")

def sign_up(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/play/')
    if request.POST:
        email = request.POST.get('email_id', None)
        password = request.POST.get('password', None)
        first_name = request.POST.get('first_name', None)
        last_name = request.POST.get('last_name', None)
        
        
        try:
            usr = User.objects.get(email=email)
            return HttpResponse(json.dumps({'success': False, 'msg': 'User with this email already exists'}))
        except:
            usr = None
        if len(password) < 10:
            return HttpResponse(json.dumps({'success': False, 'msg': 'Password should be 10 characters long.'}))

        if not first_name or not last_name:
            return HttpResponse(json.dumps({'success': False, 'msg': 'Please Enter First Name and Last Name'}))
        
        user = User.objects.create_user(email, email, password)
        if user:
            user.first_name = first_name
            user.last_name = last_name
            user.save()
            account_information_obj = Account_Information()
            account_information_obj.user = user
            account_information_obj.save()
            
            login(request, user)
            return HttpResponse(json.dumps({'success': True}))
        else:
            return HttpResponse(json.dumps({'success': True}))
    return render(request, "base/signup.html")

@login_required
def spin_machine(request):
    if request.POST:
        user = request.user
        try:
            account_information_obj = Account_Information.objects.get(user=user)
        except:
            account_information_obj = None
            return HttpResponse(json.dumps({'success': False, 'msg': 'Please Try Again.'}))

        number_of_lines_to_bet = request.POST.get('no_of_lines', None)
        amount_per_line = request.POST.get('bet_amount', None)
        try:
            balance = account_information_obj.current_month_balance
        except:
            balance = 0
        

        try:
            number_of_lines_to_bet = int(number_of_lines_to_bet)
            amount_per_line = int(amount_per_line)
        except:
            return HttpResponse(json.dumps({'success': False, 'msg': 'Please Enter numeric values only.'}))

        
        if number_of_lines_to_bet > 3 or number_of_lines_to_bet < 1:
            return HttpResponse(json.dumps({'success': False, 'msg': 'You can bet on maximum of 3 lines and minimum of 1 line.'}))
        
        
        current_bet = number_of_lines_to_bet * amount_per_line
        if current_bet > balance:
            return HttpResponse(json.dumps({'success': False, 'msg': 'You do not have sufficient balance to place this bet.'}))

        balance = balance - current_bet
        grid = create_grid_of_chars()
        winning_points, wins = calculate_winning_points(grid, number_of_lines_to_bet)
        balance = balance + winning_points
        account_information_obj.current_month_balance = balance
        account_information_obj.no_of_wins = account_information_obj.no_of_wins + wins
        account_information_obj.save()
        html = ''
        
        for row in grid:
            html +='<div class="row">'
            for col in row:
                html += '<div class="col">'+col+'</div>'
            html +='</div>'
        return HttpResponse(json.dumps({
            'success': True, 
            'html': mark_safe(html),
            'winning_points': winning_points,
            'balance': account_information_obj.current_month_balance,
            'wins': account_information_obj.no_of_wins
            }))


def login_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/play/')
    if request.POST:
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return HttpResponse(json.dumps({'success': True}))
        else:
            return HttpResponse(json.dumps({'success': False, 'msg':'Please user correct Email and Password'}))
    return render(request, "base/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')
