from django.shortcuts import render, redirect
from django.http import request
from django.contrib import messages
from teacher.models import Student,Subject,Semester,Marks
from django.contrib.auth.models import User

no_of_students = Student.objects.filter().count()
no_of_subjects = Subject.objects.filter().count()
no_of_semesters = Semester.objects.filter().count()
no_of_teachers = User.objects.count()


def indexPage(request):
    context = {
        'no_of_students': no_of_students,
        'no_of_subjects': no_of_subjects,
        'no_of_semesters': no_of_semesters,
        'no_of_teachers': no_of_teachers    
    }

    # for checking and redirecting to the mark page.
    if(request.method=="POST"):
        roll_no = request.POST.get('keyword')
        student = Student.objects.filter(roll_no=roll_no)
        if(student):
            return redirect('Markpage',roll_no = roll_no)
        else :
            messages.info(request, 'Student not found')

    return render(request,'index.html',context)



def markPage(request,roll_no):
    
    mark_list = {}
    student = Student.objects.get(roll_no = roll_no)
    for semester in Semester.objects.all().order_by('semester_number'):
        
        # Here subject__semester gives all the subjects of the semester by relation in django.
        semester_marks = Marks.objects.filter(student=student,subject__semester = semester)

        if semester_marks.exists():
            mark_list[semester] = semester_marks

    context = {
        'no_of_students': no_of_students,
        'no_of_subjects': no_of_subjects,
        'no_of_semesters': no_of_semesters,
        'no_of_teachers': no_of_teachers,
        'student_name' : student.student_name,
        'mark_list': mark_list,
    }
    return render(request,'student-marks.html',context)






def aboutPage(request):
    return render(request,'about.html')




def contactPage(request):
    return render(request,'contact.html')