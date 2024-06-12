from django.shortcuts import render
from myproject.config_params import char_values, frequency
from .utils import create_grid_of_chars

# Create your views here.

def slot_machine(request):
    grid = create_grid_of_chars()
    
    return render(request, "base/slot_machine.html", {'grid':grid})
