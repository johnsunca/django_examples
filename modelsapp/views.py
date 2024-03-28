from django.http import HttpResponse
from django.shortcuts import render
from .models import Department, Employee, OneCard, Project, Report 
from django.db.models import F, Q 

# Create your views here.

from datetime import date, time, datetime

def index(request):
    page = '<a href="">index</a><br>'
    page += '<a href="create">create</a><br>'
    page += '<a href="read">read</a><br>'
    page += '<a href="update">update</a><br>'
    page += '<a href="delete">delete</a><br>'
    page += '<a href="create_relations">create_relations</a><br>'
    page += '<a href="read_relations">read_relations</a><br>'
    page += '<a href="update_relations">update_relations</a><br>'
    return HttpResponse(page)


def create(request):
    Employee.objects.all().delete()
    OneCard.objects.all().delete()
    Department.objects.all().delete()
    Report.objects.all().delete()
    Project.objects.all().delete()

    # +. CRUD-No relationship

    # 1. Create: ================================================================================
    # - instantiate and save()
    # - create(), bulk_create()
    # - access fields: obj.fieldname

    # - instantiate and save()
    e = Employee(employee_id=9751234, first_name='Alex', last_name='Paul', hire_date='2010-02-03', 
                 email='alex@example.com', salary=34567.89, title='SE', level=7)
    e.save()
    e = Employee(employee_id=9751235, first_name='Bob', last_name='David', title='FE')
    e.save()
    e = Employee(employee_id=9751236, first_name='Cindy', last_name='Smith', title='BE')
    e.save()

    # - create()
    e = Employee.objects.create(employee_id=9751239, first_name='Fahad', last_name='Tusman')

    # - bulk_create()
    es = Employee.objects.bulk_create([
        Employee(employee_id=9751240, first_name='Fahad', last_name='Tusman'),
        Employee(employee_id=9751241, first_name='George', last_name='Lasdi'),
        Employee(employee_id=9751242, first_name='Hannah', last_name='Wuju'),
    ])
    es = Employee.objects.bulk_create([
        Employee(employee_id=9751243, first_name='Anna', last_name='Davad', title='SE', 
                 hire_date='2015-04-08', email='anna@example.com', salary=11223.89, level=5),
        Employee(employee_id=9751244, first_name='Banna', last_name='Davad', title='BE', 
                 hire_date='2022-05-08', email='banna@example.com', salary=22334.89, level=3),
        Employee(employee_id=9751245, first_name='Canna', last_name='Davad', title='FE', 
                 hire_date='2007-03-08', email='canna@example.com', salary=55778.89, level=4),
    ])

    page = '<a href="">index</a><br>'
    page += '<a href="create">create</a><br>'
    page += '<a href="read">read</a><br>'
    page += '<a href="update">update</a><br>'
    page += '<a href="delete">delete</a><br>'
    page += '<a href="create_relations">create_relations</a><br>'
    page += '<a href="read_relations">read_relations</a><br>'
    page += '<a href="update_relations">update_relations</a><br>'
    return HttpResponse(page)


def read(request):
    # 2. Read/Retrieve: ================================================================================
    # - all(), filter(), exclude(), order_by(), chaining filters
    # - count(), indexing[0], slicing[0:1:2], list(queryset), .values()
    # - get()
    # - F(field) and Q(condition1) | Q(condition2)
    # - .objects.aggregate(Avg(field)/Max(field)/Min(field))

    # - all(), filter(), exclude(), order_by(), chaining filters
    es1 = Employee.objects.filter(id=1)
    es2 = Employee.objects.filter(pk=2)
    es3 = Employee.objects.filter(level__range=(4, 8))
    es3 = Employee.objects.filter(id__lt=5)
    es4 = Employee.objects.filter(level__gte=3, employee_id__gte=9751240)
    es5 = Employee.objects.filter(first_name__contains='nna').exclude(first_name='Canna')
    es6 = Employee.objects.filter(last_name__in=('Davad', 'David')).order_by('salary')
    es7 = Employee.objects.filter(hire_date__year__lt=2020)
    es8 = Employee.objects.order_by("-hire_date").filter(id__gt=5)
    print(es1, es2, es3, es4, es5, es6, es7, es8, sep='\n--------\n')
    es = Employee.objects.order_by("-hire_date").filter(id__gt=5)
    # - count(), indexing[0], slicing[0:1:2], list(queryset), .values()
    print(es.count(), es[0].first_name)    
    es = Employee.objects.all() 
    print(es, list(es), es.values(), es.count(), es[0], es[0::2], sep='\n-----\n')

    # - get()
    e = Employee.objects.get(employee_id=9751236)
    e.hire_date = date(2018, 8, 9)
    e.save()
    print(e, e.first_name, e.last_name, e.full_name, e.hire_date, e.department, e.hire_status(), sep=', ')

    # - F(field) and Q(condition1) | Q(condition2)
    from django.db.models import F, Q 
    es1 = Employee.objects.filter(salary__gt=F("level") * 10000)
    es2 = Employee.objects.filter(Q(salary__gt=20000) | Q(level__gt=5))
    print(es1, es2)

    # - .objects.aggregate(Avg(field)/Max(field)/Min(field))
    from django.db.models import Avg, Max, Min
    avg = Employee.objects.aggregate(Avg("salary"))
    max = Employee.objects.aggregate(Max("salary"))
    min = Employee.objects.aggregate(Min("salary"))
    print(avg, max, min)

    page = '<a href="">index</a><br>'
    page += '<a href="create">create</a><br>'
    page += '<a href="read">read</a><br>'
    page += '<a href="update">update</a><br>'
    page += '<a href="delete">delete</a><br>'
    page += '<a href="create_relations">create_relations</a><br>'
    page += '<a href="read_relations">read_relations</a><br>'
    page += '<a href="update_relations">update_relations</a><br>'
    return HttpResponse(page)


def update(request):
    # 3. Update: ================================================================================
    # - retrieve-reassign-save() 
    # - update()

    e = Employee.objects.get(employee_id=9751234)
    e.hire_date = '2012-03-04'
    e.save()
    print(e)

    print(Employee.objects.first().salary)
    c = Employee.objects.update(salary=F('salary') * 1.1)
    print(c, Employee.objects.first().salary)

    page = '<a href="">index</a><br>'
    page += '<a href="create">create</a><br>'
    page += '<a href="read">read</a><br>'
    page += '<a href="update">update</a><br>'
    page += '<a href="delete">delete</a><br>'
    page += '<a href="create_relations">create_relations</a><br>'
    page += '<a href="read_relations">read_relations</a><br>'
    page += '<a href="update_relations">update_relations</a><br>'
    return HttpResponse(page)


def delete(request):
    # 4. Delete: ================================================================================
    # - obj.delete(), queryset.delete()
    
    e = Employee.objects.last()
    c1 = e.delete()
    es = Employee.objects.filter(id__lt=1)
    c2 = es.delete()
    print(c1, c2)

    page = '<a href="">index</a><br>'
    page += '<a href="create">create</a><br>'
    page += '<a href="read">read</a><br>'
    page += '<a href="update">update</a><br>'
    page += '<a href="delete">delete</a><br>'
    page += '<a href="create_relations">create_relations</a><br>'
    page += '<a href="read_relations">read_relations</a><br>'
    page += '<a href="update_relations">update_relations</a><br>'
    return HttpResponse(page)


def create_relations(request):
    # +. CRUD-Relationships (related objects)

    # 1. Create: ================================================================================
    # - save(), create()
    # - 1:1 save(), create()
    # - M:1 save(), create(), _set.add(), _set.create(), _set.set()
    # - M:N add(), create(), set(), _set.add(), _set.create(), _set.set()

    # 1.1 1:1 save() or create()
    e = Employee.objects.create(employee_id='78923456', first_name='alex', last_name='balex')
    c = OneCard(number=325001, card_type='SC', issued_date='2022-12-23', employee=e)
    c.save()
    
    e = Employee.objects.create(employee_id='78923457', first_name='alex', last_name='balex')
    c = OneCard.objects.create(number=325002, card_type='VC', issued_date='2021-11-13', employee=e)
    c = OneCard.objects.create(number=325003, card_type='VC', photo=False, issued_date='2023-07-11', 
                               employee=Employee.objects.get(employee_id=9751236))

    # 1.2.a M:1 assign & save(), create(arg=related object) ==========================
    d = Department.objects.create(name='Mobile Web Apps', 
                                 description='Native mobile web application R&D')
    e = Employee.objects.get(employee_id=9751234)
    e.department = d 
    e.save()
    print(e)

    e = Employee.objects.get(employee_id=9751234)
    r = Report.objects.create(title='Bug 12.34 fixed', report_date='2023-02-03', 
                              content='Fixing the bug using a 3rd package', employee=e)
    e = Employee.objects.get(employee_id=9751235)
    r = Report.objects.create(title='Bug 13.10 fixed', employee=e)

    # 1.2.b M:1 backward, use _set.add(), _set.create(), _set.set() ==========================
    d = Department.objects.get(name='Mobile Web Apps')
    e = Employee.objects.get(employee_id=9751235)
    d.employee_set.add(e)
    d.employee_set.create(employee_id=9751238, first_name='Edward', last_name='Majalo')

    d = Department.objects.get(name='Mobile Web Apps')
    e1 = Employee.objects.get(employee_id=9751236)
    e2 = Employee.objects.get(employee_id=9751235)
    d.employee_set.set([e1, e2])

    e = Employee.objects.get(employee_id=9751238)
    r = Report.objects.get(title='Bug 13.10 fixed')
    e.report_set.add(r)
    e.report_set.create(title='Bug 14.79 fixed')
    
    e1 = Employee.objects.get(employee_id=9751235)
    r1 = Report.objects.create(title='Bug 15.48 fixed', employee=e1)
    e2 = Employee.objects.get(employee_id=9751236)
    r2 = Report.objects.get(title='Bug 13.10 fixed')
    e2.report_set.set([r1, r2])

    # 1.3.a M:N add(), create(), set() ==========================
    p = Project.objects.create(name='ABC Bank Portal')
    e1 = Employee.objects.get(employee_id=9751234)
    e2 = Employee.objects.get(employee_id=9751235)
    p.employees.add(e1, e2)

    p = Project.objects.get(name='ABC Bank Portal')
    p.employees.create(employee_id=9751237, first_name='Dave', last_name='Woodman')

    p = Project.objects.get(name='ABC Bank Portal')
    e1 = Employee.objects.get(employee_id=9751234)
    e3 = Employee.objects.get(employee_id=9751236)
    p.employees.set([e1, e3])

    # 1.3.b M:N backward, use _set.add(), _set.create(), _set.set() ==========================
    e = Employee.objects.get(employee_id=9751234)
    p = Project.objects.create(name='XYZ Co. Payroll')
    e.project_set.add(p)
    e.project_set.create(name='LMN Ltd. HR System')
    e = Employee.objects.get(employee_id=9751238)
    p = Project.objects.all()
    e.project_set.set(list(p))
    e = Employee.objects.get(employee_id=9751236)
    p = Project.objects.get(name='XYZ Co. Payroll')
    e.project_set.set([p])

    page = '<a href="">index</a><br>'
    page += '<a href="create">create</a><br>'
    page += '<a href="read">read</a><br>'
    page += '<a href="update">update</a><br>'
    page += '<a href="delete">delete</a><br>'
    page += '<a href="create_relations">create_relations</a><br>'
    page += '<a href="read_relations">read_relations</a><br>'
    page += '<a href="update_relations">update_relations</a><br>'
    return HttpResponse(page)


def read_relations(request):
    # 2. Read/Retrieve: ================================================================================
    # - "follow" relationships lookups (forward and backward, using __)
    # - M:1 & M:N related object set: _set.

    # M:1
    print('-----------------------------------')
    es1 = Employee.objects.filter(department__id=2)
    es2 = Employee.objects.filter(department__name__icontains='mobile')
    es3 = Employee.objects.filter(report__title__icontains='bug', report__employee__id__gt=0).distinct() # remove duplicates
    ds1 = Department.objects.filter(employee__last_name__iexact='davad')
    e = Employee.objects.first()
    ds2 = Department.objects.filter(employee=e)
    rs1 = Report.objects.filter(employee__id=3)
    print(es1, es2, es3, ds1, ds2, rs1, sep='\n--------\n')

    # M:N
    es4 = Employee.objects.filter(project__id=3)
    ps1 = Project.objects.filter(employees__id__gte=3)

    # 1:1
    e = Employee.objects.filter(onecard__id=1)
    c = OneCard.objects.filter(employee__id=1)
    print(es4, ps1, e, c, sep='\n--------------\n')
    
    # M:1 _set.
    es = Employee.objects.filter(id__gt=4)
    es.update(department=Department.objects.last())
    d = Department.objects.first()
    es = d.employee_set.all()
    print(es.count())

    # M:N _set.
    es = Employee.objects.first()
    c1 = es.project_set.count()
    ps = Project.objects.last()
    c2 = ps.employees.count()
    print(c1, c2)

    page = '<a href="">index</a><br>'
    page += '<a href="create">create</a><br>'
    page += '<a href="read">read</a><br>'
    page += '<a href="update">update</a><br>'
    page += '<a href="delete">delete</a><br>'
    page += '<a href="create_relations">create_relations</a><br>'
    page += '<a href="read_relations">read_relations</a><br>'
    page += '<a href="update_relations">update_relations</a><br>'
    return HttpResponse(page)


def update_relations(request):
    # 3. Update: ================================================================================
    # - update(fk=obj)
    # - related object set: remove(objs), clear()

    rs = Report.objects.filter(id__lt=3)
    e = Employee.objects.last()
    c = rs.update(employee=e)
    print(c)

    # - this doesn't delete, but move out
    # M:1 _set.remove(objs) and _set.clear()
    d1 = Department.objects.create(name='temp')
    e1 = Employee.objects.create(employee_id=1000, first_name='abc1', last_name='xyz1', department=d1)
    e2 = Employee.objects.create(employee_id=1001, first_name='abc2', last_name='xyz2', department=d1)
    e3 = Employee.objects.create(employee_id=1002, first_name='abc3', last_name='xyz3', department=d1)
    d1 = Department.objects.get(name='temp')
    e1 = Employee.objects.get(employee_id=1000)
    e2 = Employee.objects.get(employee_id=1001)
    e3 = Employee.objects.get(employee_id=1002)
    d1.employee_set.remove(e1, e2, e3) # or .clear()

    # M:N remove(objs) and clear(), _set.remove(objs) and _set.clear()
    p1 = Project.objects.create(name='proj1')
    p2 = Project.objects.create(name='proj2')
    p3 = Project.objects.create(name='proj3')
    p1 = Project.objects.get(name='proj1')
    p2 = Project.objects.get(name='proj2')
    p3 = Project.objects.get(name='proj3')    
    e1 = Employee.objects.get(employee_id=1000)
    e2 = Employee.objects.get(employee_id=1001)
    e3 = Employee.objects.get(employee_id=1002)
    p1.employees.add(e1, e2, e3)
    p2.employees.add(e1, e2, e3)
    p3.employees.add(e1, e2, e3)
    p1.employees.remove(e1)
    e2.project_set.remove(p2)
    p3.employees.clear()
    e2.project_set.clear()

    page = '<a href="">index</a><br>'
    page += '<a href="create">create</a><br>'
    page += '<a href="read">read</a><br>'
    page += '<a href="update">update</a><br>'
    page += '<a href="delete">delete</a><br>'
    page += '<a href="create_relations">create_relations</a><br>'
    page += '<a href="read_relations">read_relations</a><br>'
    page += '<a href="update_relations">update_relations</a><br>'
    return HttpResponse(page)

from .models import Location, School, Teacher, Course

def exercises(request):

    Location.objects.all().delete()
    School.objects.all().delete()
    Teacher.objects.all().delete()
    Course.objects.all().delete()

    # Exercise 1 - basics, 1:1

    # Create some locations
    location1 = Location.objects.create(address="123 Main St", city="New York")
    location2 = Location.objects.create(address="456 Elm St", city="Los Angeles")
    location3 = Location.objects.create(address="789 Elm St", city="Los Angeles")
    location4 = Location.objects.create(address="123 Elm St", city="Los Angeles")
    location5 = Location.objects.create(address="789 King St", city="Los Angeles")
    location6 = Location.objects.create(address="123 King St", city="Los Angeles")
    location7 = Location.objects.create(address="222 King St", city="Los Angeles")

    # Create some schools
    school1 = School.objects.create(name="P.S. 101", location=location1, type="preliminary")
    school2 = School.objects.create(name="Lincoln High School", location=location2, type="high")
    school3 = School.objects.create(name="Yes High School", location=location3, type="high")
    school4 = School.objects.create(name="A.P.S. 101", location=location4, type="preliminary")
    school5 = School.objects.create(name="A.Lincoln High School", location=location5, type="high")
    school7 = School.objects.create(name="A.Lincoln High School", location=location7, type="high")

    # Get all locations, schools
    all_locations = Location.objects.all()
    all_schools = School.objects.all()

    # Get the first ones
    first_location = Location.objects.first()
    first_school = School.objects.first()

    # Given an address, get the location
    location_by_address = Location.objects.filter(address="123 Main St").first()

    # Given a city, get the locations
    locations_by_city = Location.objects.filter(city="New York")

    # Given a location, get the school
    school_by_location = School.objects.get(location=location1)

    # Given a name, get the school
    school_by_name = School.objects.get(name="P.S. 101")

    # Given a type, get the schools
    schools_by_type = School.objects.filter(type="high")

    # Get the school at the first location
    school_at_first_location = School.objects.get(location=first_location)

    # Given an address, get the school at that address
    school_at_address = School.objects.get(location__address="123 Main St")

    # Given a city, get the schools in it
    schools_in_city = School.objects.filter(location__city="New York")

    # Get the location of the first school
    location_of_first_school = first_school.location

    # Given a school name, get the location of it
    location_of_school_by_name = School.objects.get(name="P.S. 101").location

    # Given a school type, get the locations of it
    locations_of_schools_by_type = School.objects.filter(type="high").values_list('location', flat=True)

    # Change the location of a school
    school_to_change_location = School.objects.get(name="P.S. 101")
    school_to_change_location.location = location6
    school_to_change_location.save()

    # Change the school of a location
    location_to_change_school = Location.objects.get(address="123 Main St")
    location_to_change_school.school = school2
    location_to_change_school.save()

    # Delete the last location
    last_location = Location.objects.last()
    last_location.delete()

    # Delete the last school
    last_school = School.objects.last()
    last_school.delete()    
    

    # Exercise 2 - M:1

    # Create some teachers
    school1 = School.objects.all()[0]
    school2 = School.objects.all()[1]
    teacher1 = Teacher.objects.create(name="John Smith", email="john@example.com", school=school1)
    teacher2 = Teacher.objects.create(name="Jane Doe", email="jane@example.com", school=school2)

    # Get all teachers
    all_teachers = Teacher.objects.all()

    # Given an email, get the teacher
    teacher_by_email = Teacher.objects.get(email="john@example.com")

    # Given a school name, get the teachers
    teachers_by_school_name = Teacher.objects.filter(school__name="P.S. 101")

    # Given a school type, get the teachers
    teachers_by_school_type = Teacher.objects.filter(school__type="high")

    # Given a city, get the teachers
    teachers_by_city = Teacher.objects.filter(school__location__city="New York")

    # Given a teacher, get the school location
    teacher = Teacher.objects.get(name="John Smith")
    school_location_of_teacher = teacher.school.location

    # Given a school, get the teachers
    teachers_of_school = Teacher.objects.filter(school=school1)
    teachers_of_school1 = school1.teacher_set.all()

    # Given a school, get the teachers whose names are "Jack"
    teachers_named_jack = Teacher.objects.filter(name="Jack", school=school1)
    teachers_named_jack1 = school1.teacher_set.filter(name="Jack")

    # Get the schools having a teacher named "Jack"
    schools_with_teacher_jack = School.objects.filter(teacher__name="Jack")

    # Remove a given teacher from a given school
    teacher_to_remove = school1.teacher_set.first()
    school1.teacher_set.remove(teacher_to_remove)

    # Change the email of the first teacher
    first_teacher = Teacher.objects.first()
    first_teacher.email = "john.smith@example.com"
    first_teacher.save()

    # Change the school of the second teacher
    second_teacher = Teacher.objects.all()[1]  # Assuming there are at least 2 teachers
    second_teacher.school = school1
    second_teacher.save()

    # Delete the last teacher
    last_teacher = Teacher.objects.last()
    last_teacher.delete()

    # Exercise 3 - M:N

    # Create some courses
    course1 = Course.objects.create(name="Math", credit=3)
    course2 = Course.objects.create(name="Science", credit=4)

    # Create some teachers
    teacher1 = Teacher.objects.create(name="John Smith", email="john@example.com")
    teacher2 = Teacher.objects.create(name="Jane Doe", email="jane@example.com")

    # Assign courses to teachers
    course1.teachers.add(teacher1)
    course1.teachers.add(teacher2)
    course2.teachers.add(teacher2)

    # Get all courses
    all_courses = Course.objects.all()

    # Given a name, get the course
    course_by_name = Course.objects.get(name="Math")

    # Given a course, get the teachers
    teachers_of_course = course1.teachers.all()

    # Given a teacher, get the courses
    courses_of_teacher1 = teacher1.course_set.all()

    # Given a teacher email, get the courses
    teacher_email = "john@example.com"
    courses_of_teacher_email = Course.objects.get(teachers__email=teacher_email)

    # Get the courses that are taught by teachers named "Jack"
    courses_taught_by_jack = Course.objects.filter(teachers__name="Jack")

    # Get the teachers who teach courses of credit 3
    teachers_of_credit_3_courses = Teacher.objects.filter(course__credit=3)

    # Remove a given teacher from a given course
    course1.teachers.remove(teacher1)

    # Remove a given course from a given teacher
    teacher1.course_set.remove(course2)

    # Given a teacher, clear all courses assigned to him
    teacher_to_clear_courses = Teacher.objects.first()
    teacher_to_clear_courses.course_set.clear()

    page = '<a href="index">index</a><br>'
    page += '<a href="create">create</a><br>'
    page += '<a href="read">read</a><br>'
    page += '<a href="update">update</a><br>'
    page += '<a href="delete">delete</a><br>'
    return HttpResponse(page)