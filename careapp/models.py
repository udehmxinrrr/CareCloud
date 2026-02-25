from django.db import models

# Create your models here.
class PatientS(models.Model):
    firstname = models.CharField(max_length=200)
    lastname = models.CharField(max_length=200)
    DOB = models.DateField()
    age = models.IntegerField()
    gender = models.CharField(max_length=20)
    dateregistered = models.DateTimeField()
    medicalhistory = models.TextField()

    def __str__(self):
        return self.firstname + " " + self.lastname



class Doctors(models.Model):
    firstname = models.CharField(max_length=200)
    lastname = models.CharField(max_length=200)
    tel = models.CharField(max_length=24)
    email = models.EmailField()
    Specialization = models.CharField(max_length=100)

    def __str__(self):
        return self.firstname + " " + self.lastname + " " + self.Specialization



class Appointment(models.Model):
    Name = models.CharField(max_length=200)
    email = models.EmailField()
    Phone = models.CharField(max_length=20)
    datetime = models.DateTimeField()
    Department = models.CharField(max_length=100)
    Doctor = models.CharField(max_length=100)
    Message = models.TextField()

    def __str__(self):
        return self.Name
