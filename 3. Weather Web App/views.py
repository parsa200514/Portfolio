"""
Definition of views.
"""

from django.shortcuts import render
from app.forms import Location_Input
from app import logic

def index(request):
    location=''
    weather=''
    form = Location_Input()
    
    if request.method == 'POST':
        
        form = Location_Input(request.POST)
        if form.is_valid():
                location = form.cleaned_data['location']
                weather = logic.Weather_Data(location)
                

    
    context ={
        'form':form,
        'weather':weather,
        
    }
    
    return render(request, 'app/index.html', context)



