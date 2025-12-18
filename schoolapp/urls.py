from django.urls import path
from . import views


urlpatterns = [
   path('',views.home, name='home'),
   path('signin/',views.signin_view, name='signin'),
   # path('signup/',views.signup_view, name='signup'),
   
   
   # HOMEPAGE
   
   path('gallery/', views.gallery_view,name='gallery'),
   path('Contact/', views.contact_view,name='contact'),
   
   
   # DASHBOARD
   path('dashboard/', views.dashboard_view,name='dashboard'),
   
   
  #  TEACHERS
  path('dashboard/teacher_list/', views.teacher_list, name='teacher_list'),
  path('dashboard/teachers/create/', views.teacher_create, name='teacher_create'),
  path('teachers/edit/<int:id>/', views.update_teacher, name='teacher_edit'),
  
  
  
  # STUDENTS
  path('dashboard/student_list/', views.student_list, name='student_list'),
  path('dashboard/students/create/', views.student_create, name='student_create'),
  path('students/edit/<int:id>/', views.update_student, name='student_edit'),
  
  
  
  # SUBJECTS
  
  path('dashboard/subject_list/', views.subject_list, name='subject_list'),
  path('dashboard/subject/create', views.subject_create, name='subject_create'),
  path('subjects/edit/<int:subject_id>/', views.subject_update, name='subject_update'),
  
  
  
  
  # CLASSROOM
  path('dashboard/classroom_list/', views.classroom_list, name='classroom_list'),
  path('dashboard/classroom/create/', views.classroom_create, name='classroom_create'),
  path('classrooms/edit/<int:id>/', views.update_classroom, name='classroom_edit'),
  
  
  
#   RESULTS

path('dashboard/results/', views.result_list, name='result_list'),
path('dashboard/result_create/', views.result_create, name='result_create'),
path('results/edit/<int:result_id>/', views.result_update, name='result_update'),









# CASHIER

path('dashboard/cashier/', views.cashier_list, name='cashier_list'),
path('dashboard/cashier/create/', views.cashier_create, name='cashier_create'),
path('cashiers/edit/<int:cashier_id>/', views.cashier_update, name='cashier_update'),







#  FEES

path('dashboard/fees/', views.fee_list, name='fee_list'),
path('dashboard/fees/create', views.fees_create, name='fees_create'),
path('fees/edit/<int:fee_id>/', views.fee_update, name='fee_update'),


#  LOGOUT
   
path('logout/', views.logout_view,name='logout'),



#  DELETE VIEWS

path('delete_teacher/<int:id>/', views.delete_teacher, name='delete_teacher'),
path('delete_student/<int:id>/', views.delete_student, name='delete_student'),
path('delete_subject/<int:id>/', views.delete_subject, name='delete_subject'),
# path('delete_cashier/<int:id>/', views.delete_cashier, name='delete_cashier'),
path('delete_classroom/<int:id>/', views.delete_classroom, name='delete_classroom'),
path('delete_fees/<int:id>/', views.delete_fees, name='delete_fees'),
path('delete_result/<int:id>/', views.delete_result, name='delete_result'),




#  GENERATE RESULT

path('result_report/', views.result_report, name='result_report'),


]
