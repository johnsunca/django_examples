from django.contrib import admin

# Register your models here.

from .models import Department, Student, Subject, Enrollment, Setting


# guest account: guest1/HelloDjango

# simple customization
admin.site.site_title = 'Student Management System - Admin'
admin.site.site_header = 'Student Management System - Admin'
admin.site.index_title = 'Student Management System - Index'

class StudentAdmin(admin.ModelAdmin):
    list_display = ['student_id', 'name', 'date_of_birth', 'department', 'is_international']
    list_filter = ['department', 'is_international']
    date_hierarchy = 'date_of_birth'
admin.site.register(Student, StudentAdmin)

# - inlines
class StudentInline(admin.TabularInline):
    model = Student 
class DepartmentAdmin(admin.ModelAdmin):    
    inlines = [StudentInline, ]
    list_display = ['code', 'name', 'campus']
admin.site.register(Department, DepartmentAdmin)

class SubjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'credit']
    list_filter = ['credit']
admin.site.register(Subject, SubjectAdmin)

class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ['student', 'subject', 'mark', 'enroll_date']
    search_fields = ['student__name', 'subject__name']
admin.site.register(Enrollment, EnrollmentAdmin)

admin.site.register(Setting)