from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('student', 'Студент'),
        ('teacher', 'Викладач'),
        ('admin','Адміністратор'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student', verbose_name="Роль")

class Announcement(models.Model):
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    content = models.TextField(verbose_name="Текст оголошення")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата створення")

    def __str__(self):
        return self.title

class Course(models.Model):
    title = models.CharField(max_length=200, verbose_name="Назва")
    description = models.TextField(verbose_name="Опис")
    price = models.IntegerField(default=0, verbose_name="Ціна (грн)")
    duration = models.CharField(max_length=50, default="4 тижні", verbose_name="Тривалість")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Module(models.Model):
    course = models.ForeignKey(Course, related_name='modules', on_delete=models.CASCADE)
    title = models.CharField(max_length=200, verbose_name="Назва модуля")

    def __str__(self):
        return self.title
    
class Lesson(models.Model):
    module = models.ForeignKey(Module, related_name='lessons', on_delete=models.CASCADE)
    title = models.CharField(max_length=200, verbose_name="Тема уроку")
    content = models.TextField(verbose_name="Текст уроку")
    video_url = models.URLField(blank=True, null=True, verbose_name="Посилання на відео (YouTube)")
    image = models.ImageField(upload_to='lesson_images/', blank=True, null=True, verbose_name="Зображення")
    
    def __str__(self):
        return self.title
    
class Submission(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField(verbose_name="Ваша відповідь")
    grade = models.PositiveIntegerField(null=True, blank=True, verbose_name="Оцінка")
    feedback = models.TextField(blank=True, verbose_name="Коментар викладача")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student} - {self.lesson}"
    
class Enrollment(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    enrolled_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'course') 

    def __str__(self):
        return f"{self.student} -> {self.course}"