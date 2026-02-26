from django.shortcuts import render, redirect, get_object_or_404

from careapp.models import Appointment


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

def delete(request, id):
    appoint = Appointment.objects.get(id=id)
    appoint.delete()
    return redirect('/show')
def edit(request, id):
    editappointment = get_object_or_404 (Appointment, id=id)

    if request.method == 'POST':
        editappointment.Name = request.POST['name']
        editappointment.email = request.POST['email']
        editappointment.Phone = request.POST['phone']
        editappointment.datetime = request.POST['date']
        editappointment.Department = request.POST['department']
        editappointment.Doctor = request.POST['doctor']
        editappointment.Message = request.POST['message']
        editappointment.save()
        return redirect('/show')
    else:
        return render(request, 'edit.html', {'editappointment': editappointment})
