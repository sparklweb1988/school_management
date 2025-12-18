from django.db import models
from django.contrib.auth.models import AbstractUser

# Custom User model extending AbstractUser
class User(AbstractUser):
    STATUS = (
        ('admin', 'Admin'),
        ('teacher', 'Teacher'),
        ('cashier', 'Cashier'),
        ('student', 'Student'),
    )
    role = models.CharField(max_length=20, choices=STATUS, default='student')

    def __str__(self):
        return self.username

# Subject model: represents a subject in the school
class Subject(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    teacher = models.ForeignKey('Teacher', on_delete=models.SET_NULL, null=True, blank=True, related_name='taught_subjects')  # Renamed reverse relation

    def __str__(self):
        return self.name

# SchoolClass model: represents a grade or class in the school
class SchoolClass(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    teacher = models.ForeignKey('Teacher', on_delete=models.SET_NULL, null=True, blank=True)  # Teacher for the class

    def __str__(self):
        return self.name

# Student model: stores information about each student
class Student(models.Model):
    user_profile = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    school_class = models.ForeignKey(SchoolClass, on_delete=models.SET_NULL, null=True, blank=True)  # One student to one class
    date_of_birth = models.DateField()
    date_joined = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user_profile.username

# Teacher model: stores information about each teacher
class Teacher(models.Model):
    user_profile = models.OneToOneField(User, on_delete=models.CASCADE, related_name='teacher_profile')
    subjects = models.ManyToManyField(Subject, related_name='assigned_teachers')  # Renamed reverse relation
    date_of_joining = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user_profile.username
    
    
    
    
class Term(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    
    def __str__(self):
        return self.name

# Result model: stores student results for each subject
class Result(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, blank=True)  # Added Teacher reference
    test_1 = models.FloatField()
    test_2 = models.FloatField()
    exam = models.FloatField()
    date = models.DateTimeField(auto_now_add=True)
    session = models.CharField(max_length=100)
    term = models.ForeignKey(Term, on_delete=models.SET_NULL, null=True, blank=True)

    @property
    def Total(self):
        return self.test_1 + self.test_2 + self.exam

    def __str__(self):
        return f"{self.student.user_profile.username} - {self.subject.name}"

# FeePayment model: stores payment details for students, handled by Cashier
class FeePayment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date_of_payment = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=100)
    payment_status = models.CharField(max_length=20, choices=[('Paid', 'Paid'), ('Pending', 'Pending')], default='Pending')
    cashier = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, limit_choices_to={'role': 'cashier'})

    def __str__(self):
        return f"Payment by {self.student.user_profile.username} - {self.amount} (Processed by {self.cashier.username if self.cashier else 'Unknown'})"
