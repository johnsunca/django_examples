from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse

from .forms import ReportForm, StudentModelForm, EnrollmentModelForm
from .models import Department, Setting, Student, Subject, Enrollment
from django.utils import timezone
from faker import Faker
import random
from django.contrib.auth.decorators import (
    user_passes_test,
    permission_required,
    login_required,
)

# stage1: read and delete

def home(request):
    stagevalue = Setting.objects.filter(name='stage')[0].value
    stage = str(stagevalue) if stagevalue else '1'
    request.session['stage'] = 'stage' + stage
    print(request.session['stage'])
    return redirect('studentmgmtsys:list_students')


@user_passes_test(lambda u: u.is_superuser)
def insert_test_data(request):
    fake = Faker()

    # Delete existing records from all tables
    Department.objects.all().delete()
    Student.objects.all().delete()
    Subject.objects.all().delete()
    Enrollment.objects.all().delete()

    # Generate and save departments
    campus_choices = ['brampton', 'mississauga', 'oakville']
    from .constants import departments
    for i in range(len(departments)):
        campus = random.choice(campus_choices)
        Department.objects.create(
            name=departments[i]['name'],
            code=departments[i]['code'],
            campus=campus
        )

    # Generate and save students
    department_choices = []
    for i in range(30):
        department = fake.random_element(elements=Department.objects.all())
        Student.objects.create(
            name=fake.name(),
            student_id=f'S{97531+i}',
            date_of_birth=fake.date_of_birth(minimum_age=18, maximum_age=25),
            address=fake.address(),
            department=department,
            is_international=fake.boolean(chance_of_getting_true=20)
        )

    # Generate and save subjects
    from .constants import subjects
    for i in range(len(subjects)):
        Subject.objects.create(
            name=subjects[i],
            credit=random.randint(1, 4)
        )

    # Generate and save enrollments
    students = Student.objects.all()
    subjects = Subject.objects.all()
    for i in range(150):
        student = fake.random_element(elements=students)
        subject = fake.random_element(elements=subjects)
        Enrollment.objects.create(
            student=student,
            subject=subject,
            mark=round(random.uniform(0, 100), 2),
            enroll_date=fake.date()
        )

    return redirect('studentmgmtsys:home')  # Redirect to home page after data insertion


# Function-based view for listing departments
def department_list(request):
    departments = Department.objects.all().order_by('name')
    return render(request, 'studentmgmtsys/department_list.html', {'departments': departments})

# # Function-based view for department detail
# def department_detail(request, department_id):
#     department = get_object_or_404(Department, pk=department_id)
#     return render(request, 'studentmgmtsys/department_detail.html', {'department': department})

# # Function-based view for deleting department
@user_passes_test(lambda u: u.is_superuser)
def delete_department(request, department_id):
    department = get_object_or_404(Department, pk=department_id)
    if department:
        department.delete()
    return redirect('studentmgmtsys:list_departments')

# Function-based view for listing students
def student_list(request):
    students = Student.objects.all().order_by('student_id')
    return render(request, 'studentmgmtsys/student_list.html', {'students': students})

# Function-based view for student detail
def student_detail(request, student_id):
    student = get_object_or_404(Student, pk=student_id)
    return render(request, 'studentmgmtsys/student_detail.html', {'student': student})

# Function-based view for deleting student
@user_passes_test(lambda u: u.is_superuser)
def delete_student(request, student_id):
    student = get_object_or_404(Student, pk=student_id)
    if student:
        student.delete()
    return redirect('studentmgmtsys:list_students')  

# Function-based view for listing subjects
def subject_list(request):
    subjects = Subject.objects.all().order_by('name')
    return render(request, 'studentmgmtsys/subject_list.html', {'subjects': subjects})

# # Function-based view for subject detail
# def subject_detail(request, subject_id):
#     subject = get_object_or_404(Subject, pk=subject_id)
#     return render(request, 'studentmgmtsys/subject_detail.html', {'subject': subject})

# # Function-based view for deleting subject
@user_passes_test(lambda u: u.is_superuser)
def delete_subject(request, subject_id):
    subject = get_object_or_404(Subject, pk=subject_id)
    if subject:
        subject.delete()
    return redirect('studentmgmtsys:list_subjects')

# Function-based view for listing enrollments
def enrollment_list(request):
    enrollments = Enrollment.objects.all().order_by('student__student_id')
    return render(request, 'studentmgmtsys/enrollment_list.html', {'enrollments': enrollments})

# # Function-based view for enrollment detail
# def enrollment_detail(request, enrollment_id):
#     enrollment = get_object_or_404(Enrollment, pk=enrollment_id)
#     return render(request, 'studentmgmtsys/enrollment_detail.html', {'enrollment': enrollment})

# Function-based view for deleting enrollment
@user_passes_test(lambda u: u.is_superuser)
def delete_enrollment(request, enrollment_id):
    enrollment = get_object_or_404(Enrollment, pk=enrollment_id)
    if enrollment:
        enrollment.delete()
    return redirect('studentmgmtsys:list_enrollments') 

# ============================================================================

def search(request):
    departments = Department.objects.all()
    subjects = Subject.objects.all()
    return render(request, 'studentmgmtsys/search.html',  
                  {'departments': departments, 'subjects': subjects}) 

# Function-based view for searching for students
def search_students(request):
    students = Student.objects.all().order_by('name')

    if 'student_id' in request.GET and request.GET['student_id'].strip():
        students = students.filter(student_id=request.GET['student_id'])
    if 'name' in request.GET and request.GET['name'].strip():
        students = students.filter(name__icontains=request.GET['name'])
    if 'birth_year' in request.GET and request.GET['birth_year'].strip() and request.GET['birth_year'].isdigit():
        students = students.filter(date_of_birth__year=int(request.GET['birth_year']))
    if 'address' in request.GET and request.GET['address'].strip():
        students = students.filter(address__icontains=request.GET['address'])
    if 'department' in request.GET and request.GET['department'].strip():
        students = students.filter(department__id=request.GET['department'])
    if 'campus' in request.GET and request.GET['campus'].strip():
        students = students.filter(department__campus=request.GET['campus'])
    if 'is_international' in request.GET and request.GET.get('is_international').strip():
        is_international = request.GET.get('is_international').strip()
        if is_international == 'international': students = students.filter(is_international=True)
        elif  is_international == 'domestic': students = students.filter(is_international=False)
    if 'subject' in request.GET and request.GET['subject'].strip():
        students = students.filter(subjects__id=request.GET['subject'])    

    return render(request, 'studentmgmtsys/search_results.html', {'students': students})

def search_students_by_department(request, department_id):
    students = Student.objects.filter(department__id=department_id).order_by('name')
    return render(request, 'studentmgmtsys/search_results.html', 
                  {'students': students, 'search_key': f'Department: {Department.objects.get(id=department_id)}'})

def search_students_by_subject(request, subject_id):
    students = Student.objects.filter(subjects=subject_id).order_by('name')
    return render(request, 'studentmgmtsys/search_results.html', 
                  {'students': students, 'search_key': f'Subject: {Subject.objects.get(id=subject_id)}'})

def search_enrollments_by_subject(request, subject_id):
    enrollments = Enrollment.objects.filter(subject_id=subject_id).order_by('student__name')
    return render(request, 'studentmgmtsys/enrollment_search_results.html', 
                  {'enrollments': enrollments, 'search_key': f'Subject: {Subject.objects.get(id=subject_id)}'})

def search_enrollments_by_student(request, student_id):
    enrollments = Enrollment.objects.filter(student__id=student_id).order_by('student__name')
    return render(request, 'studentmgmtsys/enrollment_search_results.html', 
                  {'enrollments': enrollments, 'search_key': f'Student: {Student.objects.get(id=student_id)}'})

# ============================================================================

# stage2: create and update

@user_passes_test(lambda u: u.is_superuser)
def student_edit(request, student_id=None):
    # If pk is provided, it's an update operation, otherwise it's a create operation
    # If GET method, it's for an empty form for create or initial form for update
    # If POST method, it can be for creating a new student or updating an existing student
    student = get_object_or_404(Student, pk=student_id) if student_id else None

    if request.method == 'POST':
        form = StudentModelForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect('studentmgmtsys:list_students')  
    else:
        form = StudentModelForm(instance=student)

    context = {'form': form, 'student': student}

    if 'edit' in request.path or 'update' in request.path:
        context['students'] = Student.objects.all()
        
    return render(request, 'studentmgmtsys/student_form.html', context)


@user_passes_test(lambda u: u.is_superuser)
def enrollment_edit(request, enrollment_id=None):
    enrollment = get_object_or_404(Enrollment, pk=enrollment_id) if enrollment_id else None

    if request.method == 'POST':
        form = EnrollmentModelForm(request.POST, instance=enrollment)
        if form.is_valid():
            form.save()
            return redirect('studentmgmtsys:list_enrollments')  
    else:
        form = EnrollmentModelForm(instance=enrollment)

    context = {'form': form, 'enrollment': enrollment}

    if 'edit' in request.path or 'update' in request.path:
        context['enrollments'] = Enrollment.objects.all()
        
    return render(request, 'studentmgmtsys/enrollment_form.html', context)


def report(request):
    context = {'data': {}}    
    form = ReportForm(request.GET)
    if form.is_valid():
        context['name'] = form.cleaned_data['name']
        context['email'] = form.cleaned_data['email']
        if form.cleaned_data['title']:
            context['title'] = '== REPORT =='
        context['notes'] = form.cleaned_data['notes']
        context['color'] = form.cleaned_data['color']

        models = form.cleaned_data['models']
        if 'department' in models: 
            context['data']['Departments'] = Department.objects.count()
            context['data']['Brampton Departments'] = Department.objects.filter(campus='brampton').count()
            context['data']['Mississauga Departments'] = Department.objects.filter(campus='mississauga').count()
            context['data']['Oakville Departments'] = Department.objects.filter(campus='oakville').count()
        if 'student' in models: 
            context['data']['Students'] = Student.objects.count()
            context['data']['International Students'] = Student.objects.filter(is_international=True).count()
            context['data']['Domestic Students'] = Student.objects.filter(is_international=False).count()
            context['data']['Born Before 2000'] = Student.objects.filter(date_of_birth__year__lt='2000').count()
            context['data']['Born After 2000'] = Student.objects.filter(date_of_birth__year__gte='2000').count()
        if 'subject' in models: 
            context['data']['Subjects'] = Subject.objects.count()
        if 'enrollment' in models: 
            context['data']['Enrollments'] = Enrollment.objects.count()
            from django.db.models import Avg
            context['data']['Average Mark'] = round(list(Enrollment.objects.aggregate(Avg('mark')).values())[0], 2)
    elif 'submit' not in request.GET:
        print('here')
        form = ReportForm()
    context['form'] = form   
    return render(request, 'studentmgmtsys/report.html', context)
