from django.shortcuts import render
from myproject.config_params import char_values, frequency
from .utils import create_grid_of_chars, calculate_winning_points
from django.http import HttpResponse
import json
from django.utils.safestring import mark_safe

# Create your views here.

def slot_machine(request):
    grid = create_grid_of_chars()
    return render(request, "base/slot_machine.html", {'grid':grid})

def spin_machine(request):
    if request.POST:
        number_of_lines_to_bet = request.POST.get('no_of_lines', None)
        amount_per_line = request.POST.get('bet_amount', None)
        balance = request.POST.get('balance', None)
        if balance:
            balance = int(balance)

        if not number_of_lines_to_bet or not amount_per_line:
            return HttpResponse(json.dumps({'success': False, 'msg': 'Please select both values.'}))
        if int(number_of_lines_to_bet) > 3 or int(number_of_lines_to_bet) < 1:
            return HttpResponse(json.dumps({'success': False, 'msg': 'Please choose a number between 1 and 3'}))
        #check for float points also
        
        current_bet = int(number_of_lines_to_bet) * int(amount_per_line)
        if current_bet > balance:
            return HttpResponse(json.dumps({'success': False, 'msg': 'You do not have sufficient balance to place this bet.'}))

        balance = balance - current_bet
        grid = create_grid_of_chars()
        winning_points = calculate_winning_points(grid)
        balance = balance + winning_points
        html = ''
        for row in grid:
            html+='<div>'
            for col in row:
                html += '<div class="col">%s</div>'%(col)
            html+='</div>'
        return HttpResponse(json.dumps({
            'success': True, 
            'html': mark_safe(html),
            'winning_points': winning_points,
            'balance': balance
            }))

