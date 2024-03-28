from django import forms
from studentmgmtsys.models import Student, Enrollment

class StudentModelForm(forms.ModelForm):
    class Meta:
        model = Student 
        fields = '__all__'
        labels = {'student_id': 'Student ID',
                  'is_international': 'International', 
                  'subjects': 'Subjects enrolled'}
        widgets = {'date_of_birth': forms.DateInput(attrs={'type': 'date'})}


class EnrollmentModelForm(forms.ModelForm):
    class Meta:
        model = Enrollment 
        fields = '__all__'
        widgets = {'mark': forms.NumberInput(attrs={'step': '0.1', 'min': '0.0', 'value': '3.5'})}
        widgets = {'enroll_date': forms.DateInput(attrs={'type': 'date'})}


class ReportForm(forms.Form):
    COLOR_CHOICES = (('', 'Default'), ('red', 'Red'), ('brown', 'Brown'), ('blue', 'Blue'), ('green', 'Green'), ('grey', 'Grey'))
    MODEL_CHOICES = (('department', 'Department'), ('student', 'Student'), ('subject', 'Subject'), ('enrollment', 'Enrollment') )
    name = forms.CharField(max_length=50)
    email = forms.EmailField(required=False)
    title = forms.BooleanField(required=False)
    models = forms.MultipleChoiceField(choices=MODEL_CHOICES)
    notes = forms.CharField(widget=forms.Textarea, required=False)
    color = forms.ChoiceField(choices=COLOR_CHOICES, required=False)

    