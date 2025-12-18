from django.contrib import admin
from .models import Term, User, SchoolClass, Subject, Teacher, Student, Result, FeePayment



# Register your models here.




class FeePaymentAdmin(admin.ModelAdmin):
    list_display = ('student', 'amount', 'payment_method', 'payment_status', 'cashier', 'date_of_payment')

admin.site.register(User)
admin.site.register(SchoolClass)
admin.site.register(Subject)
admin.site.register(Teacher)
admin.site.register(Student)
admin.site.register(Result)
admin.site.register(FeePayment, FeePaymentAdmin)
admin.site.register(Term)
