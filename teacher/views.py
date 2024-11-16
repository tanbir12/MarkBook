from django.shortcuts import render, redirect
from django.http import request
from django.contrib import messages
from teacher.models import Student,Subject,Semester,Marks,TeacherSubject
from django.contrib.auth.models import User
from django.http import HttpResponse
from .forms import addStudent_form,StudentMarksForm,addSuperuserForm
from django.forms import formset_factory
from django.contrib.auth.decorators import login_required

no_of_students = Student.objects.filter().count()
no_of_subjects = Subject.objects.filter().count()
no_of_semesters = Semester.objects.filter().count()
no_of_teachers = User.objects.count()

#  ++++++++++++++++++++++++++++++++++  View Functions  +++++++++++++++++++++++++++++++++++++++






# ++++++++++++++++++++++++++++++++++  Profile View  +++++++++++++++++++++++++++++++++++++++
@login_required
def profilePage(request):
    admin_name = request.user
    subjects = TeacherSubject.objects.filter(teacher = admin_name)
    teachers = User.objects.all()
    context = {
        'no_of_students': no_of_students,
        'no_of_subjects': no_of_subjects,
        'no_of_semesters': no_of_semesters,
        'no_of_teachers': no_of_teachers,
        'admin' : admin_name,
        'subjects': subjects,
        'teachers': teachers,
    }

    # form for requestting student marks and redirect using course year.
    if request.method == 'POST':
        subject_id = request.POST.get('RadioOptions')    
        course_year = request.POST.get('course_year')

        try:
            students = Student.objects.filter(course_year = course_year)
            return redirect('add-marks',year = course_year,teacher_id = admin_name.id,subject_id = subject_id)

        except Student.DoesNotExist:
            messages.error(request, 'No students found In This Course Year')


    return render(request,'profile.html',context)







# ++++++++++++++++++++++++++++++++++  Subject View  +++++++++++++++++++++++++++++++++++++++
@login_required
def manageSubject(request):
    # subject add/remove to user.

    subjects = Subject.objects.all().order_by('id')
    admin_name = request.user
    teacher_subjects = TeacherSubject.objects.filter(teacher = admin_name)
    context = {
        'subjects' : subjects,
        'teacher_subjects' : teacher_subjects,
    }

    if request.method == "POST":
        subject_id = request.POST.get('subject_id')
        option = request.POST.get('RadioOptions')
        
        try:
            subject = Subject.objects.get(id=int(subject_id))
        except Subject.DoesNotExist:
            messages.error(request, 'Subject does not exist')
            return render(request,'add_subject.html',context)
        if option == 'add':
            TeacherSubject.objects.get_or_create(teacher = admin_name,subject=subject)

        if option == 'remove':
            TeacherSubject.objects.filter(teacher = admin_name,subject=subject).delete()

    # subjects add/remove to database.
    return render(request,'add_subject.html',context)










# ++++++++++++++++++++++++++++++++++ Add Student View  +++++++++++++++++++++++++++++++++++++++
@login_required
def addStudent(request):
    if(request.method=="POST"):
        form = addStudent_form(request.POST)
        if form.is_valid():
            form.save();
            messages.success(request,'Student Successfully Added.')
            return render(request,'student/add_student.html',{'form':form})
        else :
           messages.info(request,'Student Already Exists.') 
    else:
        form = addStudent_form()
    return render(request,'student/add_student.html',{'form':form})









# ++++++++++++++++++++++++++++++++++ Add Teacher View  +++++++++++++++++++++++++++++++++++++++
@login_required
def addTeacher(request):
    if request.method == 'POST':
        form = addSuperuserForm(request.POST)
        if form.is_valid():
            user = User.objects.create_superuser(
                first_name = form.cleaned_data['first_name'],
                last_name = form.cleaned_data['last_name'],
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password']
            )
            messages.success(request, "Teacher created successfully!")
        else:
            messages.error(request, "There was an error creating the Teacher.")
    else:
        form = addSuperuserForm()
    return render(request, 'registration/create_superuser.html', {'form': form})






# ++++++++++++++++++++++++++++++++++ Delete Teacher View  +++++++++++++++++++++++++++++++++++++++
@login_required
def deleteTeacher(request):
    # Check if the user making the request is also a superuser
    if request.user.is_superuser:
    # Get the user with the given user_id and check if they are a superuser
        if request.method == "POST":
            user_id = request.POST.get('user_id')
            
            try:
                user_to_delete = User.objects.get(id=int(user_id))
                if(user_to_delete.is_superuser):
                    user_to_delete.delete()

            except User.DoesNotExist:
                messages.error(request, "Incorrect Admin ID.")



    return render(request,'registration/remove_superuser.html')



# function takes year  and subject as input and returns the list of subjects for that semester marks input
@login_required
def add_marks_view(request, year, subject_id, teacher_id):
    # Fetch students in the specified year
    students = Student.objects.filter(course_year=year)
    teacher = User.objects.get(id=teacher_id)
    subject = Subject.objects.get(id=subject_id)

    # Prepare formset with initial data for each student
    StudentMarksFormSet = formset_factory(StudentMarksForm, extra=0)
    initial_data = [{'roll_no': student.roll_no, 'student_name': student.student_name} for student in students]


    if(request.method == 'POST'):
        formset = StudentMarksFormSet(request.POST,initial=initial_data)
        if formset.is_valid():
            # Save marks for each student
            for form in formset:
                roll_no = form.cleaned_data['roll_no']
                marks_obtained = form.cleaned_data['marks_obtained']
                student = Student.objects.get(roll_no=roll_no)

                # Create or update the marks for each student
                Marks.objects.create(
                    student=student,
                    subject=subject,
                    teacher=teacher,
                    marks_obtained=marks_obtained, 
                    grade=calculate_grade(marks_obtained)
                )
            return render(request, 'student/add_marks.html', { 'formset': formset,'subject': subject,'year': year,'teacher': teacher})
        


    else:
        # Render empty formset with student information for the first GET request
        formset = StudentMarksFormSet(initial=initial_data)
    
    return render(request, 'student/add_marks.html', {
        'formset': formset,
        'subject': subject,
        'year': year,
        'teacher': teacher
    })













#  __________________________________Extra Functions for various purposes_________________________


# function for  calculating grade based on marks
def calculate_grade(marks_obtained):
    if marks_obtained >= 90:
        return 'A'
    elif marks_obtained >= 80:
        return 'B'
    elif marks_obtained >= 70:
        return 'C'
    elif marks_obtained >= 60:
        return 'D'
    else:
        return 'F'