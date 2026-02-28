from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from core import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index_view, name='home'),
    path('index.html', views.index_view),
    path('courses/', views.courses_list_view, name='courses_list'),
    path('courses.html', views.courses_list_view),
    path('register/', views.register_view, name='register'),
    path('register.html', views.register_view),
    path('course/<int:course_id>/', views.course_detail_view, name='course_detail'),
    path('course/<int:course_id>/enroll/', views.enroll_course_view, name='enroll_course'),
    path('course/<int:course_id>/learn/', views.course_learn_view, name='course_learn'),
    path('teacher/dashboard/', views.teacher_dashboard_view, name='teacher_dashboard'),
    path('profile/', views.profile_view, name='profile'),
    path('submission/<int:submission_id>/grade/', views.grade_submission, name='grade_submission'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('course/add/', views.CourseCreateView.as_view(), name='course_create'),
    path('course/<int:pk>/edit/', views.CourseUpdateView.as_view(), name='course_edit'),
    path('course/<int:pk>/delete/', views.CourseDeleteView.as_view(), name='course_delete'),
    path('course/<int:course_id>/module/add/', views.ModuleCreateView.as_view(), name='module_create'),
    path('module/<int:module_id>/lesson/add/', views.LessonCreateView.as_view(), name='lesson_create'),
    path('lesson/<int:pk>/delete/', views.LessonDeleteView.as_view(), name='lesson_delete'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)