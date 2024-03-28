
# ======================================================
# More example model and model form and views

from django import forms
from django.db import models

from django.shortcuts import get_object_or_404, redirect, render

class Person(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]

    MARITAL_STATUS_CHOICES = [
        ('S', 'Single'),
        ('M', 'Married'),
        ('D', 'Divorced'),
        ('W', 'Widowed'),
    ]

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    age = models.PositiveIntegerField()
    marital_status = models.CharField(max_length=1, choices=MARITAL_STATUS_CHOICES)
    spouse = models.OneToOneField('self', on_delete=models.SET_NULL, blank=True, null=True)
    children = models.ManyToManyField('self', related_name='parents', blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class PersonModelForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ['first_name', 'last_name', 'gender', 'age', 'marital_status', 'spouse', 'children']

        labels = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'gender': 'Gender',
            'age': 'Age',
            'marital_status': 'Marital Status',
            'spouse': 'Spouse',
            'children': 'Children',
        }

        widgets = {
            'age': forms.NumberInput(attrs={'step': '1', 'min': '0'}),
            'marital_status': forms.RadioSelect(),
            'spouse': forms.TextInput(attrs={'placeholder': 'Enter spouse name'}),
            'children': forms.SelectMultiple(attrs={'class': 'custom-select'}),
        }

def person_list(request):
    persons = Person.objects.all()
    return render(request, 'myapp/person_list.html', 
                  {'persons': persons})

def person_detail(request, pk):
    person = get_object_or_404(Person, pk=pk)
    return render(request, 'myapp/person_detail.html', 
                  {'person': person})

def person_delete(request, pk):
    person = get_object_or_404(Person, pk=pk)
    if request.method == 'POST':
        person.delete()
        return redirect('person_list')
    
    return render(request, 'myapp/person_delete.html', 
                  {'person': person})

def person_edit(request, pk=None):
    person = get_object_or_404(Person, pk=pk) \
        if pk else None
    
    if request.method == 'POST':
        form = PersonModelForm(request.POST, 
                               instance=person)
        if form.is_valid():
            form.save()
            return redirect('person_list')
    else:
        form = PersonModelForm(instance=person)

    return render(request, 'myapp/person_form.html', 
                  {'form': form, 'person': person})