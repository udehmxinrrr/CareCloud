from django.shortcuts import render

from careapp.models import *

# Create your views here.
def home(request):
    return render(request, 'index.html')

def starter(request):
    return render(request, 'starter-page.html')

def appointments(request):
    if request.method == 'POST':
        all = Appointment(
            Name = request.POST['Name'],
            email = request.POST['email'],
            Phone = request.POST['Phone '],
            datetime = request.POST['datetime'],
            Department = request.POST['Department'],
            Doctor = request.POST['Doctor'],
            Message = request.POST['Message'],

        )
        all.save()
        return render(request, 'appointments.html')

    else:
        return render(request, 'appointments.html')



def about(request):
    return render(request, 'about.html')