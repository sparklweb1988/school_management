from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import logout, login, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model


User = get_user_model()

from schoolapp.models import FeePayment, Result, SchoolClass, Student, Subject, Teacher, Term


# HOME PAGE

def home(request):
    return render(request, 'hompage/home.html')


def gallery_view(request):
    return render(request, 'hompage/gallery.html')


def contact_view(request):
    return render(request, 'hompage/contact.html')


# SIGNIN

def signin_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)  # Logs in the user

            # Check role using the authenticated user object
            if user.is_superuser:
                return redirect('dashboard')  # Admin dashboard

            elif getattr(user, 'role', None) == 'teacher':
                return redirect('dashboard')  # Teacher dashboard

            elif getattr(user, 'role', None) == 'cashier':
                return redirect('dashboard')  # Cashier dashboard

            elif getattr(user, 'role', None) == 'student':
                return redirect('dashboard')  # Student dashboard

            else:
                return redirect('dashboard')  # fallback

        else:
            return render(request, 'accounts/signin.html', {'error': 'Invalid credentials'})

    return render(request, 'accounts/signin.html')


# DASHBOARD

def dashboard_view(request):
    total_teachers = Teacher.objects.count()
    total_students = Student.objects.count()
    toatl_classroom = SchoolClass.objects.count()
    total_subjects = Subject.objects.count()
    total_results = Result.objects.count()
    total_fees = FeePayment.objects.count()
    context = {
        'total_teachers':total_teachers,
        'total_students':total_students,
        'toatl_classroom':toatl_classroom,
        'total_subjects':total_subjects,
        'total_results':total_results,
        'total_fees':total_fees,
        
    }
    return render(request, 'dashboard/dashboard.html',context)


# TEACHER VIEW

def teacher_list(request):
    teachers = Teacher.objects.all()
    context = {
        'teachers': teachers
    }
    return render(request, 'dashboard/teacher_list.html', context)





def teacher_create(request):
    subjects = Subject.objects.all()

    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Subjects (multiple)
        subject_ids = request.POST.getlist('subjects')

        # Create user
        user = User.objects.create_user(
            username=username,
            password=password,
            email=email,
            first_name=first_name,
            last_name=last_name,
        )

        # Create teacher
        teacher = Teacher.objects.create(user_profile=user)
        teacher.subjects.set(subject_ids)

        return redirect('teacher_list')

    return render(request, 'dashboard/teacher_create.html', {
        'subjects': subjects
    })


# UPDATE TEACHER


def update_teacher(request, id):
    teacher = get_object_or_404(Teacher, id=id)  # Fetch the teacher object
    user = teacher.user_profile  # Get associated user object
    subjects = Subject.objects.all()  # All subjects for the select field

    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Subjects (multiple)
        subject_ids = request.POST.getlist('subjects')

        # Update user details
        user.first_name = first_name
        user.last_name = last_name
        user.username = username
        user.email = email

        if password:  # Only update password if it's provided
            user.set_password(password)

        user.save()  # Save the user

        # Update teacher details
        teacher.subjects.set(subject_ids)  # Update the subjects
        teacher.save()  # Save the teacher

        return redirect('teacher_list')  # Redirect to teacher list page

    # Pre-fill the form with the existing teacher data
    return render(request, 'dashboard/update_teacher.html', {
        'teacher': teacher,
        'subjects': subjects,
    })


# STUDENT VIEW

def student_list(request):
    students = Student.objects.select_related('user_profile', 'school_class').all()
    return render(request, 'dashboard/student_list.html', {
        'students': students
    })


def student_create(request):
    
    classes = SchoolClass.objects.all()
    error = None

    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        date_of_birth = request.POST.get('date_of_birth')
        class_id = request.POST.get('school_class')

        # Check if username exists
        if User.objects.filter(username=username).exists():
            error = "Username already exists."
        else:
            user = User.objects.create_user(
                username=username,
                password=password,
                email=email,
                first_name=first_name,
                last_name=last_name,
            )

            student = Student.objects.create(
                user_profile=user,
                date_of_birth=date_of_birth,
                school_class_id=class_id if class_id else None
            )

            return redirect('student_list')

    return render(request, 'dashboard/student_create.html', {
        'classes': classes,
        'error': error
    })
    
    
    #  STUDENT UPDATE
    
    
def update_student(request, id):
    student = get_object_or_404(Student, id=id)  # Fetch the student object
    user = student.user_profile  # Get the associated user object
    classes = SchoolClass.objects.all()  # All classes for the select field
    error = None

    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        date_of_birth = request.POST.get('date_of_birth')
        class_id = request.POST.get('school_class')

        # Check if the username already exists
        if User.objects.filter(username=username).exclude(id=user.id).exists():
            error = "Username already exists."
        else:
            # Update user details
            user.first_name = first_name
            user.last_name = last_name
            user.username = username
            user.email = email

            if password:  # Only update password if it's provided
                user.set_password(password)

            user.save()  # Save the user

            # Update student details
            student.date_of_birth = date_of_birth
            student.school_class_id = class_id if class_id else None
            student.save()  # Save the student

            return redirect('student_list')  # Redirect to student list page

    return render(request, 'dashboard/update_student.html', {
        'student': student,
        'classes': classes,
        'error': error,
    })





# SUBJECT VIEW

def subject_list(request):
   
    if request.user.is_superuser:  # Admin
        # Admin can see all subjects
        subjects = Subject.objects.all()
    
    elif request.user.role == 'teacher':
        # Teacher sees only subjects they teach
        teacher = Teacher.objects.get(user_profile=request.user)
        subjects = teacher.subjects.all()
    
    elif request.user.role == 'student':
        # Student sees only subjects they are enrolled in
        student = Student.objects.get(user_profile=request.user)
        # If students are enrolled in subjects via results, you can filter subjects based on results
        subjects = Subject.objects.filter(result__student=student)
    
    else:
        subjects = []

    context = {
        'subjects': subjects,
        
    }

    return render(request, 'dashboard/subject_list.html', context)





def subject_create(request):
   
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('desc', '')  # Default empty string
        teacher_ids = request.POST.getlist('teacher')  # Get list of selected teacher IDs

        if not name:
            return render(request, 'dashboard/subject_create.html', {'error': 'Name is required'})

        # Create the Subject object
        subject = Subject.objects.create(name=name, description=description)

        # If teachers are selected, assign them to the subject
        if teacher_ids:
            teachers = Teacher.objects.filter(id__in=teacher_ids)
            subject.teachers.set(teachers)  # Assign multiple teachers

        return redirect('subject_list')

    # Query all teachers to display in the form
    teachers = Teacher.objects.all()

    # Render the form with teachers context
    return render(request, 'dashboard/subject_create.html', {'teachers': teachers})


#  UPDATE SUBJECT VIEW

def subject_update(request, subject_id):
    # Get the subject object by ID
    subject = get_object_or_404(Subject, id=subject_id)
    
    teachers = Teacher.objects.all()  # Fetch all teachers
    error = None

    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('desc', '')  # Default empty string
        teacher_ids = request.POST.getlist('teacher')  # Get list of selected teacher IDs

        # Check if name is provided
        if not name:
            error = 'Subject name is required.'
        else:
            # Update the subject fields
            subject.name = name
            subject.description = description

            # If teachers are selected, assign them to the subject
            if teacher_ids:
                teachers = Teacher.objects.filter(id__in=teacher_ids)
                subject.teachers.set(teachers)  # Assign multiple teachers

            subject.save()  # Save the updated subject

            return redirect('subject_list')  # Redirect to subject list page

    return render(request, 'dashboard/update_subject.html', {
        'subject': subject,
        'teachers': teachers,
        'error': error,
    })


# CLASSROOM VIEW

def classroom_list(request):
    
    if request.user.is_superuser:
        # Admin can see all classrooms
        classrooms = SchoolClass.objects.all()
    
    elif request.user.role == 'teacher':
        # Teacher sees classrooms related to the subjects they teach
        teacher = Teacher.objects.get(user_profile=request.user)
        
        # Get subjects taught by the teacher
        subjects_taught_by_teacher = teacher.taught_subjects.all()

        # Get classrooms taught by the teacher based on the subject(s) they teach
        classrooms = SchoolClass.objects.filter(teacher=teacher)
    
    elif request.user.role == 'student':
        # Student sees only the classroom they belong to
        student = Student.objects.get(user_profile=request.user)
        classrooms = SchoolClass.objects.filter(id=student.school_class.id)
    
    else:
        classrooms = []

    context = {
        'classrooms': classrooms,
        
    }

    return render(request, 'dashboard/classroom_list.html', context)




def classroom_create(request):
   
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('desc', '')  # default empty string
        teacher_id = request.POST.get('teacher')  # Get the teacher ID from the form

        if not name:
            return render(request, 'dashboard/classroom_create.html', {'error': 'Name is required'})

        # Create the SchoolClass object
        classroom = SchoolClass.objects.create(name=name, description=description)

        # If a teacher was selected, assign the teacher to the class
        if teacher_id:
            teacher = Teacher.objects.get(id=teacher_id)
            classroom.teachers.add(teacher)

        return redirect('classroom_list')

    # Query all teachers to display in the form
    teachers = Teacher.objects.all()

    # Render the form with teachers context
    return render(request, 'dashboard/classroom_create.html', {'teachers': teachers})

#  CLASSROOM UPDATE


def update_classroom(request, id):
    # Get the classroom object by ID
    classroom = get_object_or_404(SchoolClass, id=id)
    
    teachers = Teacher.objects.all()  # Fetch all teachers
    error = None

    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('desc', '')  # Default empty string
        teacher_id = request.POST.get('teacher')  # Get the selected teacher's ID

        # Check if name is provided
        if not name:
            error = 'Class name is required.'
        else:
            # Update the classroom fields
            classroom.name = name
            classroom.description = description

            # If a teacher is selected, assign that teacher to the class
            if teacher_id:
                teacher = get_object_or_404(Teacher, id=teacher_id)
                classroom.teacher = teacher  # Assign teacher to classroom

            classroom.save()  # Save the updated classroom

            return redirect('classroom_list')

    return render(request, 'dashboard/update_classroom.html', {
        'classroom': classroom,
        'teachers': teachers,
        'error': error,
    })






# RESULT VIEW

def result_list(request):
  
    if request.user.is_superuser or request.user.role == 'admin':
        results = Result.objects.all()

    elif request.user.role == 'teacher':
        results = Result.objects.filter(teacher__user_profile=request.user)

    elif request.user.role == 'student':
        student = Student.objects.filter(user_profile=request.user).first()

        if student:
            results = Result.objects.filter(student=student)
        else:
            results = []

    else:
        results = []

    return render(request, 'dashboard/result_list.html', {
        'results': results,
        
    })






def result_create(request):
   
    students = Student.objects.all()
    subjects = Subject.objects.all()

    if request.method == 'POST':
        student_id = request.POST.get('student')
        subject_id = request.POST.get('subject')
        test_1 = request.POST.get('test_1')
        test_2 = request.POST.get('test_2')
        exam = request.POST.get('exam')
        session = request.POST.get('session')

        # basic validation
        if not all([student_id, subject_id, test_1, test_2, exam, session]):
            return render(request, 'dashboard/result_create.html', {
                'students': students,
                'subjects': subjects,
                'error': 'All fields are required.'
            })

        student = Student.objects.get(id=student_id)
        subject = Subject.objects.get(id=subject_id)

        # Associate result with teacher
        teacher = subject.teacher

        Result.objects.create(
            student=student,
            subject=subject,
            teacher=teacher,
            test_1=test_1,
            test_2=test_2,
            exam=exam,
            session=session
        )

        return redirect('result_list')

    return render(request, 'dashboard/result_create.html', {
        'students': students,
        'subjects': subjects
    })



#  REULT UPDATE VIEW


def result_update(request, result_id):
    # Get the existing result by its ID
    result = get_object_or_404(Result, id=result_id)
    
    students = Student.objects.all()
    subjects = Subject.objects.all()

    if request.method == 'POST':
        student_id = request.POST.get('student')
        subject_id = request.POST.get('subject')
        test_1 = request.POST.get('test_1')
        test_2 = request.POST.get('test_2')
        exam = request.POST.get('exam')
        session = request.POST.get('session')

        # Validation to ensure all fields are filled
        if not all([student_id, subject_id, test_1, test_2, exam, session]):
            return render(request, 'dashboard/result_update.html', {
                'result': result,
                'students': students,
                'subjects': subjects,
                'error': 'All fields are required.'
            })

        # Get the student and subject objects
        student = Student.objects.get(id=student_id)
        subject = Subject.objects.get(id=subject_id)

        # Update the result fields
        result.student = student
        result.subject = subject
        result.test_1 = test_1
        result.test_2 = test_2
        result.exam = exam
        result.session = session
        
        # Save the updated result
        result.save()

        return redirect('result_list')

    # If GET request, pre-fill the form with existing result data
    return render(request, 'dashboard/update_result.html', {
        'result': result,
        'students': students,
        'subjects': subjects
    })



# CASHIER
def cashier_list(request):
    # Fetch all users with role 'cashier'
    cashiers = User.objects.filter(role='cashier')
    return render(request, 'dashboard/cashier_list.html', {'cashiers': cashiers})



def cashier_create(request):
    error = None  # Define error variable upfront

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Check if all fields are provided
        if username and email and password:
            # Create cashier user
            User.objects.create_user(
                username=username,
                email=email,
                password=password,
                role='cashier'
            )
            return redirect('cashier_list')  # Redirect to cashier list after creation
        else:
            error = "All fields are required."  # Error message if fields are missing

    # Render the template with error if POST didn't run successfully
    return render(request, 'dashboard/cashier_create.html', {'error': error})



#  UPDATE CASHIER VIEW

def cashier_update(request, cashier_id):
    # Get the existing cashier by their ID
    cashier = get_object_or_404(User, id=cashier_id, role='cashier')
    
    error = None  # Initialize error variable

    if request.method == 'POST':
        # Get form data
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Check if all required fields are provided
        if username and email and password:
            # Update cashier's details
            cashier.username = username
            cashier.email = email
            cashier.set_password(password)  # Use set_password to hash the password
            cashier.save()

            return redirect('cashier_list')  # Redirect to the cashier list after update
        else:
            error = "All fields are required."  # Error message if any field is missing

    # Render the form with the existing cashier's data
    return render(request, 'dashboard/update_cashier.html', {
        'cashier': cashier,
        'error': error
    })


# FEE PAYMENT VIEW

def fee_list(request):
    payments = FeePayment.objects.all().order_by('-date_of_payment')
    context = {
        'payments': payments,
    }
    return render(request, 'dashboard/fee_list.html', context)


def fees_create(request):
    students = Student.objects.all()
    cashiers = User.objects.filter(role='cashier')

    if request.method == 'POST':
        student_id = request.POST.get('student')
        cashier_id = request.POST.get('cashier')
        amount = request.POST.get('amount')
        payment_method = request.POST.get('payment_method')
        payment_status = request.POST.get('payment_status')

        if student_id and cashier_id and amount and payment_method and payment_status:
            FeePayment.objects.create(
                student_id=student_id,
                cashier_id=cashier_id,
                amount=amount,
                payment_method=payment_method,
                payment_status=payment_status
            )
            return redirect('fee_list')

    return render(request, 'dashboard/fees_create.html', {
        'students': students,
        'cashiers': cashiers
    })
    
    
#  UPDATE FEES VIEW



def fee_update(request, fee_id):
    fee = get_object_or_404(FeePayment, id=fee_id)  # Fetch the FeePayment object
    
    students = Student.objects.all()
    cashiers = User.objects.filter(role='cashier')
    
    error = None  # Initialize error variable

    if request.method == 'POST':
        student_id = request.POST.get('student')
        cashier_id = request.POST.get('cashier')
        amount = request.POST.get('amount')
        payment_method = request.POST.get('payment_method')
        payment_status = request.POST.get('payment_status')

        # Validate that all fields are provided
        if student_id and cashier_id and amount and payment_method and payment_status:
            # Update the fee payment object with the new data
            fee.student_id = student_id
            fee.cashier_id = cashier_id
            fee.amount = amount
            fee.payment_method = payment_method
            fee.payment_status = payment_status
            fee.save()

            return redirect('fee_list')  # Redirect to the fee list after update
        else:
            error = "All fields are required."  # Error message if any field is missing

    # Render the form with the existing fee details pre-filled
    return render(request, 'dashboard/update_fees.html', {
        'fee': fee,
        'students': students,
        'cashiers': cashiers,
        'error': error
    })

#  DELETE VIEWS

def delete_teacher(request, id):
    # Find the Teacher via User ID
    user = get_object_or_404(User, pk=id)  # First get the user by ID
    teacher = get_object_or_404(Teacher, user_profile=user)  # Find the teacher related to this user
    
    teacher.delete()  # Delete the Teacher instance
    
    return redirect('teacher_list')




def delete_student(request, id):
    user = get_object_or_404(User, pk=id) 
    student = get_object_or_404(Student, user_profile=user)
    student.delete()
    return redirect('student_list')





def delete_subject(request, id):
    subject = get_object_or_404(Subject,pk=id)
    subject.delete()
    return redirect('subject_list')






def delete_classroom(request, id):
    classroom = get_object_or_404(SchoolClass,pk=id)
    classroom.delete()
    return redirect('classroom_list')




def delete_fees(request, id):
    fees = get_object_or_404(FeePayment,pk=id)
    fees.delete()
    return redirect('fees_list')



def delete_result(request, id):
    result = get_object_or_404(Result,pk=id)
    result.delete()
    return redirect('result_list')






#  GENERATE RESULTS

def result_report(request):
    user = request.user
    results = Result.objects.none()
    students = Student.objects.all()
    classes = SchoolClass.objects.all()
    sessions = Result.objects.values_list('session', flat=True).distinct()
    
    # Fetch terms dynamically from the database
    terms = Term.objects.all()  # Fetch all terms from the Term table

    # Filters
    selected_student = request.GET.get('student')
    selected_class = request.GET.get('class')
    selected_session = request.GET.get('session')
    selected_term = request.GET.get('term')

    # Admin and Teacher filtering
    if user.is_superuser or user.role == 'admin':
        results = Result.objects.all()
    elif user.role == 'teacher':
        teacher = getattr(user, 'teacher_profile', None)
        results = Result.objects.filter(teacher=teacher)
    elif user.role == 'student':
        student = getattr(user, 'student_profile', None)
        results = Result.objects.filter(student=student)

    # Apply filters if provided
    if selected_student:
        results = results.filter(student_id=selected_student)
    if selected_class:
        results = results.filter(student__school_class_id=selected_class)
    if selected_session:
        results = results.filter(session=selected_session)
    if selected_term:
        results = results.filter(term=selected_term)

    context = {
        'results': results,
        'students': students,
        'classes': classes,
        'sessions': sessions,
        'terms': terms,
        'selected_student': selected_student,
        'selected_class': selected_class,
        'selected_session': selected_session,
        'selected_term': selected_term,
    }
    return render(request, 'dashboard/result_report.html', context)


# LOGOUT VIEW

def logout_view(request):
    logout(request)
    return redirect('home')





