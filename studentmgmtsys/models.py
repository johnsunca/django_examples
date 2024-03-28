from django.db import models

# Create your models here.

from django.db import models

class Department(models.Model):
    CAMPUS_CHOICES = [
        ('brampton', 'Brampton'),
        ('mississauga', 'Mississauga'),
        ('oakville', 'Oakville'),
    ]

    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10)
    campus = models.CharField(max_length=20, choices=CAMPUS_CHOICES)

    def __str__(self):
        return self.name + '@' + self.get_campus_display()

class Student(models.Model):
    name = models.CharField(max_length=100)
    student_id = models.CharField(max_length=20, unique=True)
    date_of_birth = models.DateField()
    address = models.CharField(max_length=200, null=True, blank=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    is_international = models.BooleanField(default=False)
    subjects = models.ManyToManyField('Subject', blank=True, through='Enrollment')

    def __str__(self):
        return self.name

class Subject(models.Model):
    name = models.CharField(max_length=100, unique=True)
    credit = models.IntegerField(default=3) 

    def __str__(self):
        return self.name

class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    mark = models.FloatField(null=True, blank=True)
    enroll_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.student} - {self.subject}: {self.mark}"

class Setting(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    value = models.CharField(max_length=100, null=True, blank=True)
