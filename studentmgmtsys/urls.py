from django.urls import path
from . import views


app_name = 'studentmgmtsys'

urlpatterns = [
    # stage 1: read, delete, search

    path('', views.home, name='home'),
    path('insert_test_data/', views.insert_test_data, name='insert_test_data'),

    path('list_departments/', views.department_list, name='list_departments'),
    # path('department/<int:department_id>/', views.department_detail, name='department_detail'),
    # path('delete_department/<int:department_id>/', views.delete_department, name='delete_department'),

    path('list_students/', views.student_list, name='list_students'),
    path('student/<int:student_id>/', views.student_detail, name='student_detail'),
    path('delete_student/<int:student_id>/', views.delete_student, name='delete_student'),

    path('list_subjects/', views.subject_list, name='list_subjects'),
    # path('subject/<int:subject_id>/', views.subject_detail, name='subject_detail'),
    # path('delete_subject/<int:subject_id>/', views.delete_subject, name='delete_subject'),

    path('list_enrollments/', views.enrollment_list, name='list_enrollments'),
    # path('enrollment/<int:enrollment_id>/', views.enrollment_detail, name='enrollment_detail'),
    path('delete_enrollment/<int:enrollment_id>/', views.delete_enrollment, name='delete_enrollment'),

    path('search/', views.search, name='search'),
    path('search_students/', views.search_students, name='search_students'),
    path('search_students_by_department/<int:department_id>/', views.search_students_by_department, name='search_students_by_department'),
    path('search_students_by_subject/<int:subject_id>/', views.search_students_by_subject, name='search_students_by_subject'),
    path('search_enrollments_by_subject/<int:subject_id>/', views.search_enrollments_by_subject, name='search_enrollments_by_subject'),
    path('search_enrollments_by_student/<int:student_id>/', views.search_enrollments_by_student, name='search_enrollments_by_student'),
    
    # stage 2: create, edit, form, admin, static

    path("student/create/", views.student_edit, name='student_create'),
    path("student/edit/", views.student_edit, name='student_edit'),
    path("student/<int:student_id>/update/", views.student_edit, name='student_update'),
    path("enrollment/create/", views.enrollment_edit, name='enrollment_create'),
    path("enrollment/edit/", views.enrollment_edit, name='enrollment_edit'),
    path("enrollment/<int:enrollment_id>/update/", views.enrollment_edit, name='enrollment_update'),

    path("report/", views.report, name='report'),
    # path("settings/", views.settings, name='settings'),

]
