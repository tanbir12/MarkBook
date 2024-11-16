from django.db import models
from django.contrib.auth.models import User  # Using Django's default User model for teachers

class Semester(models.Model):
    semester_number = models.CharField(default='First')

    def __str__(self):
        return f"Semester {self.semester_number}"

class Subject(models.Model):
    subject_name = models.CharField(max_length=50)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, related_name="subjects")

    def __str__(self):
        return self.subject_name

class Student(models.Model):
    roll_no = models.CharField(max_length=15, primary_key=True)  # Custom primary key
    student_name = models.CharField(max_length=50)
    course_year = models.IntegerField()

    def __str__(self):
        return f"{self.roll_no} - {self.student_name}"


class TeacherSubject(models.Model):
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name="subjects")
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name="teachers")

    class Meta:
        unique_together = ('teacher', 'subject')

    def __str__(self):
        return f"{self.subject.id} - {self.subject.subject_name}"

class Marks(models.Model):
    student = models.ForeignKey(Student, to_field='roll_no', on_delete=models.CASCADE, related_name="marks",db_column='student_roll_no')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name="marks")
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name="marks")
    marks_obtained = models.IntegerField()
    grade = models.CharField(max_length=2)

    def __str__(self):
        return f"{self.student.roll_no} - {self.subject} - {self.marks_obtained}"
