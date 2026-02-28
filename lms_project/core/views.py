from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Count
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView,DeleteView
from .forms import CourseForm, CustomUserCreationForm, GradingForm, SubmissionForm, UserUpdateForm,ModuleForm,LessonForm
from .models import Announcement, Course, Enrollment, Lesson, Submission,Module

class AdminOnlyRequiredMixin(UserPassesTestMixin):
    def test_func(self):

        if not self.request.user.is_authenticated:
            return False

        is_admin_role = (self.request.user.role.lower() == 'admin')
        return is_admin_role or self.request.user.is_superuser

class CourseCreateView(LoginRequiredMixin, AdminOnlyRequiredMixin, CreateView):
    model = Course
    form_class = CourseForm
    template_name = 'course_form.html'
    success_url = reverse_lazy('courses_list')

    def form_valid(self, form):
      
        form.instance.author = self.request.user
        return super().form_valid(form)

class CourseUpdateView(LoginRequiredMixin, AdminOnlyRequiredMixin, UpdateView):
    model = Course
    form_class = CourseForm
    template_name = 'course_form.html'
    success_url = reverse_lazy('courses_list')

def index_view(request):
    courses = Course.objects.all()[:3]
    try:
        announcements = Announcement.objects.order_by('-created_at')[:3]
    except:
        announcements = []
    return render(request, 'index.html', {'courses': courses, 'announcements': announcements})

def courses_list_view(request):
    courses = Course.objects.all()
    return render(request, 'courses.html', {'courses': courses})

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

@login_required
def profile_view(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UserUpdateForm(instance=request.user)
    
    user_submissions = Submission.objects.filter(student=request.user)
    enrollments = Enrollment.objects.filter(student=request.user)
    
    return render(request, 'profile.html', {
        'form': form, 
        'submissions': user_submissions,
        'enrollments': enrollments
    })


def course_detail_view(request, course_id):

    course = get_object_or_404(Course, pk=course_id)
    is_enrolled = False
    
    if request.user.is_authenticated:
        is_enrolled = Enrollment.objects.filter(student=request.user, course=course).exists()
        if is_enrolled:
            pass 

    return render(request, 'course_detail.html', {
        'course': course,
        'is_enrolled': is_enrolled
    })

@login_required
def enroll_course_view(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    Enrollment.objects.get_or_create(student=request.user, course=course)
    return redirect('course_learn', course_id=course.id)

@login_required
def course_learn_view(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    if request.user.role not in ['teacher', 'admin']:
        if not Enrollment.objects.filter(student=request.user, course=course).exists():
            return redirect('course_detail', course_id=course.id) 

    form = SubmissionForm()
    
    user_submissions = {}
    submissions = Submission.objects.filter(student=request.user, lesson__module__course=course)
    for sub in submissions:
        user_submissions[sub.lesson.id] = sub

    if request.method == 'POST' and 'submit_homework' in request.POST:
        lesson_id = request.POST.get('lesson_id')
        sub_form = SubmissionForm(request.POST)
        if sub_form.is_valid():
            submission = sub_form.save(commit=False)
            submission.student = request.user
            submission.lesson_id = lesson_id
            submission.save()
            return redirect('course_learn', course_id=course.id)

    return render(request, 'course_learn.html', {
        'course': course, 
        'form': form,
        'user_submissions': user_submissions
    })

@login_required
def teacher_dashboard_view(request):

    if request.user.role not in ['teacher', 'admin']:
        return redirect('home')

    courses = Course.objects.all()
    
    submissions_to_grade = Submission.objects.filter(grade__isnull=True).order_by('created_at')
    
    return render(request, 'teacher_dashboard.html', {
        'courses': courses,
        'submissions_to_grade': submissions_to_grade
    })

@login_required
def grade_submission(request, submission_id):
    if request.user.role not in ['teacher', 'admin']:
        return redirect('home')
        
    submission = get_object_or_404(Submission, id=submission_id)
    
    if request.method == 'POST':
        form = GradingForm(request.POST, instance=submission)
        if form.is_valid():
            form.save()
            return redirect('teacher_dashboard')
    else:
        form = GradingForm(instance=submission)
        
    return render(request, 'grade_submission.html', {'form': form, 'submission': submission})

class CourseDeleteView(LoginRequiredMixin, AdminOnlyRequiredMixin, DeleteView):
    model = Course
    template_name = 'course_confirm_delete.html'
    success_url = reverse_lazy('courses_list') 

class ModuleCreateView(LoginRequiredMixin, AdminOnlyRequiredMixin, CreateView):
    model = Module
    form_class = ModuleForm
    template_name = 'module_form.html'
    
    def form_valid(self, form):
        course = get_object_or_404(Course, pk=self.kwargs['course_id'])
        form.instance.course = course
        return super().form_valid(form)

    def get_success_url(self):

        return reverse_lazy('course_detail', kwargs={'course_id': self.kwargs['course_id']})
    
class LessonCreateView(LoginRequiredMixin, AdminOnlyRequiredMixin, CreateView):
    model = Lesson
    form_class = LessonForm
    template_name = 'lesson_form.html'
    
    def form_valid(self, form):
        module = get_object_or_404(Module, pk=self.kwargs['module_id'])
        form.instance.module = module
        return super().form_valid(form)

    def get_success_url(self):
        module = get_object_or_404(Module, pk=self.kwargs['module_id'])
        return reverse_lazy('course_detail', kwargs={'course_id': module.course.id})
    
class LessonDeleteView(LoginRequiredMixin, AdminOnlyRequiredMixin, DeleteView):
    model = Lesson
    template_name = 'lesson_confirm_delete.html'
    
    def get_success_url(self):
        course_id = self.object.module.course.id
        return reverse_lazy('course_detail', kwargs={'course_id': course_id})