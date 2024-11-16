from django import forms
from teacher.models import Student
from django.contrib.auth.models import User


class addSuperuserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    class Meta:
        model = User
        fields = ['first_name','last_name','username', 'email', 'password']
        


    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")
        
        if password != password_confirm:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data
    
    # for overriding form datas
    def __init__(self, *args, **kwargs):
        super(addSuperuserForm, self).__init__(*args, **kwargs)
        self.fields['username'].help_text = ''



class addStudent_form(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['student_name','course_year','roll_no']


class StudentMarksForm(forms.Form):
    roll_no = forms.CharField(disabled=True)  # Hidden roll_no to link marks with student
    student_name = forms.CharField(disabled=True, label="Student Name")  # Display name as non-editable
    marks_obtained = forms.IntegerField(label="Marks", required=True)