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
            Name = request.POST['name'],
            email = request.POST['email'],
            Phone = request.POST['phone'],
            datetime = request.POST['date'],
            Department = request.POST['department'],
            Doctor = request.POST['doctor'],
            Message = request.POST['message'],

        )
        all.save()
        return render(request, 'appointments.html')

    else:
        return render(request, 'appointments.html')



def about(request):
    return render(request, 'about.html')

def show(request):
    allappointments = Appointment.objects.all()
    return render(request, 'show.html', {'allappointments': allappointments})
