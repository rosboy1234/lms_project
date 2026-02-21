from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Course, Module, Lesson, Submission, Announcement, Enrollment 

class LessonInline(admin.StackedInline):
    model = Lesson
    extra = 1

class ModuleInline(admin.StackedInline):
    model = Module
    inlines = [LessonInline]
    extra = 1

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    inlines = [ModuleInline]

@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('student', 'lesson', 'grade', 'created_at')
    list_editable = ('grade',) 
    list_filter = ('grade', 'lesson')

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'enrolled_at')
    list_filter = ('course',)

admin.site.register(CustomUser, UserAdmin)
admin.site.register(Module)
admin.site.register(Lesson)
admin.site.register(Announcement)