from django import forms
from django.core import validators
from froala_editor.widgets import FroalaEditor
from .models import Announcement, Assignment, Material, Course, Department, Student, Feedback, StudentAnswer
from django.contrib.auth.forms import UserCreationForm


#Start coding all fields 

class AnnouncementForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AnnouncementForm, self).__init__(*args, **kwargs)
        self.fields['description'].required = True
        self.fields['description'].label = ''

    class Meta:
        model = Announcement
        fields = ['description']
        widgets = {
            'description': FroalaEditor(),
        }


class AssignmentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AssignmentForm, self).__init__(*args, **kwargs)
        self.fields['description'].required = True
        self.fields['description'].label = ''

        for field in self.fields.values():
            field.required = True
            field.label = ''
        self.fields['file'].required = False

    class Meta:
        model = Assignment
        fields = ('title', 'description', 'deadline', 'marks', 'file')

        # add fields if necessary 

        widgets = {
            'description': FroalaEditor(),
            'title': forms.TextInput(attrs={'class': 'form-control mt-1', 'id': 'title', 'name': 'title', 'placeholder': 'Title'}),
            'deadline': forms.DateTimeInput(attrs={'class': 'form-control mt-1', 'id': 'deadline', 'name': 'deadline', 'type': 'datetime-local'}),
            'marks': forms.NumberInput(attrs={'class': 'form-control mt-1', 'id': 'marks', 'name': 'marks', 'placeholder': 'Marks'}),
            'file': forms.FileInput(attrs={'class': 'form-control mt-1', 'id': 'file', 'name': 'file', 'aria-describedby': 'file', 'aria-label': 'Upload'}),
        }


class MaterialForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(MaterialForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = True
            field.label = ""
        self.fields['file'].required = False

    class Meta:
        model = Material
        fields = ('description', 'file')
        widgets = {
            'description': FroalaEditor(),
            'file': forms.FileInput(attrs={'class': 'form-control', 'id': 'file', 'name': 'file', 'aria-describedby': 'file', 'aria-label': 'Upload'}),
        }

class RegistrationForm(forms.Form):
    
    class Meta:
        model = Student
        fields = '__all__'

    photo = forms.ImageField(label='photo', required=False)

    time_received = forms.DateTimeField(
        label='Time Received',
        required=False,  # You can make this field optional
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'})
    )
    registration_type = forms.CharField(  # Add this field
        label='Registration',
        max_length=50
    )
    student_id = forms.CharField(
        label='Student ID',
        max_length=10,
        validators=[validators.RegexValidator(r'^\d+$', 'Please enter a valid number.')]
    )
    first_name = forms.CharField(  # Add this field
        label='First Name',
        max_length=50
    )
    middle_name = forms.CharField(
        label='Middle Name',
        max_length=50,
        required=False  # You can make this field optional
    )
    last_name = forms.CharField(
        label='Last Name',
        max_length=100
    )
    date_of_birth = forms.DateField(
        label='Date of Birth',
        required=False,  # You can make this field optional
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    place_of_birth = forms.CharField(
        label='Place of Birth',
        max_length=100,
        required=False,  # You can make this field optional
    )
    barangay = forms.CharField(
        label='Barangay',
        max_length=100,
        required=False,
    )
    gwa = forms.DecimalField(
        label='General Weighted Average',
        min_value=75,
        max_value=99,
        decimal_places=2,
        max_digits=4,
        help_text='Enter a GWA between 75 and 95 (e.g., 85.50)',
    )
    gwa_g12 = forms.DecimalField(
        label='General Weighted Average for G12',
        min_value=75,
        max_value=99,
        decimal_places=2,
        max_digits=4,
        help_text='Enter a GWA between 75 and 95 (e.g., 85.50)',
    )
    oralcom = forms.DecimalField(
        label='Oral Communication',
        min_value=75,
        max_value=99,
        decimal_places=2,
        max_digits=4,
        help_text='Enter a GWA between 75 and 95 (e.g., 85.50)',
    )
    genmath = forms.DecimalField(
        label='General Mathematics',
        min_value=75,
        max_value=99,
        decimal_places=2,
        max_digits=4,
        help_text='Enter a GWA between 75 and 95 (e.g., 85.50)',
    )
    earthscie = forms.DecimalField(
        label='Earth and Life Science',
        min_value=75,
        max_value=99,
        decimal_places=2,
        max_digits=4,
        help_text='Enter a GWA between 75 and 95 (e.g., 85.50)',
    )
    probstats = forms.DecimalField(
        label='Probability and Statistics',
        min_value=75,
        max_value=99,
        decimal_places=2,
        max_digits=4,
        help_text='Enter a GWA between 75 and 95 (e.g., 85.50)',
    )
    #For educational background in forms.py
    grade_school_name = forms.CharField(
        label='Grade School Name',
        max_length=100,
        required=False
    )
    grade_school_address = forms.CharField(
        label='Grade School Address',
        max_length=100,
        required=False
    )
    grade_school_year_graduated = forms.IntegerField(
        label='Year Graduated (Grade School)',
        required=False,
    )
    grade_school_awards_and_recognition = forms.CharField(
        label='Awards/Recognition (Grade School)',
        max_length=200,
        required=False,
    )
    junior_high_school_name = forms.CharField(
    label='Junior Highschool Name',
    max_length=100,
    required=False
    )
    junior_high_school_address = forms.CharField(
    label='Junior Highschool Address',
    max_length=100,
    required=False
    )
    junior_high_school_year_graduated = forms.IntegerField(
    label='Year Graduated (Junior Highschool)',
    required=False,
    )
    junior_high_school_awards_and_recognition = forms.CharField(
    label='Awards/Recognition (Juinor Highschool)',
    max_length=200,
    required=False,
    )

    senior_high_school_name = forms.CharField(
    label='Senior Highschool Name',
    max_length=100,
    required=False
    )
    senior_high_school_address = forms.CharField(
    label='Senior Highschool Address',
    max_length=100,
    required=False
    )
    senior_high_school_year_graduated = forms.IntegerField(
    label='Year Graduated (Senior Highschool)',
    required=False,
    )
    senior_high_school_awards_and_recognition = forms.CharField(
    label='Awards/Recognition (Senior Highschool)',
    max_length=200,
    required=False,
    )

    vocational_school_name = forms.CharField(
    label='Vocational School Name',
    max_length=100,
    required=False
    )
    vocational_school_address = forms.CharField(
    label='Vocational School Address',
    max_length=100,
    required=False
    )
    vocational_school_year_graduated = forms.IntegerField(
    label='Year Graduated (Vocational School)',
    required=False,
    )
    vocational_school_awards_and_recognition = forms.CharField(
    label='Awards/Recognition (Vocational School)',
    max_length=200,
    required=False,
    )
    #for emergency forms
    father_full_name = forms.CharField(
        label='Father Full Name',
        max_length=50,
        required=False,  # You can make this field optional
    )
    father_contact_no = forms.CharField(
        label='Father Contact No.',
        max_length=11,
        required=False,  # You can make this field optional
        widget=forms.TextInput(attrs={'pattern': '[0-9]*', 'title': 'Only numbers are allowed.'}),
    )
    father_home_add = forms.CharField(
        label='Father Home Address',
        max_length=100,
        required=False,  # You can make this field optional
    )
    father_email_add = forms.EmailField(
        label='Father Email',
        max_length=100,
        required=False
    )
    
    OCCUPATION_CHOICES = [
    ('Self-employed', 'Self-employed'),
    ('Unemployed', 'Unemployed'),
    ('Student', 'Student'),
    ('Retired', 'Retired'),
    ('Homemaker', 'Homemaker'),
    ('Other', 'Other'),
    ]

    occupation = forms.ChoiceField(
        label='Occupation',
        choices=OCCUPATION_CHOICES,
        required=False,  # You can make this field optional
    )

    INCOME_CHOICES = [
    ('Below 3000', 'Below 3000'),
    ('3000 - 5000', '3000 - 5000'),
    ('5000 - 10000', '5000 - 10000'),
    ('10000 - 20000', '10000 - 20000'),
    ('20000 - 30000', '20000 - 30000'),
    ('30000 - 40000', '30000 - 40000'),
    ('40000 - 50000', '40000 - 50000'),
    ('Above 50000', 'Above 50000'),
    ]

    income = forms.ChoiceField(
        label='Income',
        choices=INCOME_CHOICES,
        required=False,  # You can make this field optional
    )
    #for emergency forms (mother only)
    mother_full_name = forms.CharField(
        label='Mother Full Name',
        max_length=50,
        required=False,  # You can make this field optional
    )
    mother_contact_no = forms.CharField(
        label='Mother Contact No.',
        max_length=11,
        required=False,  # You can make this field optional
        widget=forms.TextInput(attrs={'pattern': '[0-9]*', 'title': 'Only numbers are allowed.'}),
    )
    MOTHOCCUPATION_CHOICES = [
    ('Self-employed', 'Self-employed'),
    ('Unemployed', 'Unemployed'),
    ('Student', 'Student'),
    ('Retired', 'Retired'),
    ('Homemaker', 'Homemaker'),
    ('Other', 'Other'),
    ]

    moth_occupation = forms.ChoiceField(
        label='Mother Occupation',
        choices=MOTHOCCUPATION_CHOICES,
        required=False,  # You can make this field optional
    )

    MOTHINCOME_CHOICES = [
    ('Below 3000', 'Below 3000'),
    ('3000 - 5000', '3000 - 5000'),
    ('5000 - 10000', '5000 - 10000'),
    ('10000 - 20000', '10000 - 20000'),
    ('20000 - 30000', '20000 - 30000'),
    ('30000 - 40000', '30000 - 40000'),
    ('40000 - 50000', '40000 - 50000'),
    ('Above 50000', 'Above 50000'),
    ]

    moth_income = forms.ChoiceField(
        label='Mother Income',
        choices=MOTHINCOME_CHOICES,
        required=False,  # You can make this field optional
    )
    mother_home_add = forms.CharField(
        label='Mother Home Address',
        max_length=100,
        required=False,  # You can make this field optional
    )
    mother_email_add = forms.EmailField(
        label='Mother Email',
        max_length=100,
        required=False
    )
    senior_high_track = forms.ChoiceField(
        label='Senior High School Track',
        choices=Student.SENIOR_HIGH_TRACK_CHOICES,
        required=False,
    )
    senior_high_track_g12 = forms.ChoiceField(
        label='Senior High School Track',
        choices=Student.SENIOR_HIGH_TRACKG12_CHOICES,
        required=False,
    )
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]

    gender = forms.ChoiceField(
        label='Gender',
        choices=GENDER_CHOICES,
        required=False,  # You can make this field optional
    )

    RELIGION_CHOICES = [
    ('Roman Catholicism', 'Roman Catholicism'),
    ('Islam', 'Islam'),
    ('Protestant Christianity', 'Protestant Christianity'),
    ('Iglesia ni Cristo', 'Iglesia ni Cristo'),
    ('Lumad and Indigenous Beliefs', 'Lumad and Indigenous Beliefs'),
    ('Buddhism', 'Buddhism'),
    ('Taoism', 'Taoism')
    ]

    religion = forms.ChoiceField(
    label='Religion',
    choices=RELIGION_CHOICES,
    required=False,  # You can make this field optional
    )
    CIVIL_STATUS_CHOICES = [
        ('Single', 'Single'),
        ('Married', 'Married'),
        ('Divorced', 'Divorced'),
        ('Widowed', 'Widowed'),
        ('Other', 'Other'),
    ]

    civil_status = forms.ChoiceField(
        label='Civil Status',
        choices=CIVIL_STATUS_CHOICES,
        required=False,  # You can make this field optional
    )

    region = forms.ChoiceField(
        label='Region',
        required=False,
    )

    province = forms.ChoiceField(
        label='Province',
        required=False,
    )

    city = forms.ChoiceField(
        label='City',
        required=False,
    )

    COURSE1_CHOICE = [
        ('Bachelor of Science in Information Technology (Information and Network Security Elective Track)', 'Bachelor of Science in Information Technology (Information and Network Security Elective Track)'),
        ('Bachelor of Science in Computer Science (Computational and Data Sciences Elective Track)', 'Bachelor of Science in Computer Science (Computational and Data Sciences Elective Track)'),
        ('Bachelor of Science in Computer Science (Application Development Elective Track)', 'Bachelor of Science in Computer Science (Application Development Elective Track)'),
        ('Bachelor of Science in Computer Science Major in Social Computing', 'Bachelor of Science in Computer Science Major in Social Computing'),
        ('Diploma in Application Development', 'Diploma in Application Development'),
        ('Diploma in Computer Network Administration', 'Diploma in Computer Network Administration'),
    
    ]

    course1 = forms.ChoiceField(
        label='Course1',
        choices=COURSE1_CHOICE,
        required=False,
    )

    COURSE2_CHOICE = [
        ('Bachelor of Science in Information Technology (Information and Network Security Elective Track)', 'Bachelor of Science in Information Technology (Information and Network Security Elective Track)'),
        ('Bachelor of Science in Computer Science (Computational and Data Sciences Elective Track)', 'Bachelor of Science in Computer Science (Computational and Data Sciences Elective Track)'),
        ('Bachelor of Science in Computer Science (Application Development Elective Track)', 'Bachelor of Science in Computer Science (Application Development Elective Track)'),
        ('Bachelor of Science in Computer Science Major in Social Computing', 'Bachelor of Science in Computer Science Major in Social Computing'),
        ('Diploma in Application Development', 'Diploma in Application Development'),
        ('Diploma in Computer Network Administration', 'Diploma in Computer Network Administration'),
    ]

    course2 = forms.ChoiceField(
        label='Course2',
        choices=COURSE2_CHOICE,
        required=False,
    )
    CITIZENSHIP_CHOICES = [
    ('Filipino Citizen', 'Filipino Citizen'),
    ('Dual Citizen', 'Dual Citizen'),
    ('Former Filipino Citizen', 'Former Filipino Citizen'),
    ('Foreign Citizen', 'Foreign Citizen'),
    ]
    citizenship = forms.ChoiceField(
        label='Citizenship',
        choices=CITIZENSHIP_CHOICES,
        required=False
    )
    contact_number = forms.CharField(
        label='Contact No.',
        max_length=11,
        required=False,  # You can make this field optional
        widget=forms.TextInput(attrs={'pattern': '[0-9]*', 'title': 'Only numbers are allowed.'}),
    )
    email = forms.EmailField(
        label='Email',
        max_length=100,
        required=False
    )
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput
    )
    confirm_password = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput
    )
    class Meta:
        model = Student
        fields = '__all__'
        widgets = {
            'time_received': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

DEPARTMENT_CHOICES = [
    ('BSIT (Information and Network Security Elective Track)', 'BSIT (Information and Network Security Elective Track)'),
    ('BSCS (Computational and Data Sciences Elective Track)', 'BSCS (Computational and Data Sciences Elective Track)'),
    ('BSCS (Application Development Elective Track)', 'BSCS (Application Development Elective Track)'),
    ('BSCS Major in Social Computing', 'BSCS Major in Social Computing'),
    ('Diploma in Application Development', 'Diploma in Application Development'),
    ('Diploma in Computer Network Administration', 'Diploma in Computer Network Administration'),
]

class FeedbackForm(forms.ModelForm):
    department = forms.ChoiceField(choices=DEPARTMENT_CHOICES)

    class Meta:
        model = Feedback
        fields = ['student_id', 'student_name', 'department', 'feedback_messages']

class StudentAnswerForm(forms.ModelForm):
    class Meta:
        model = StudentAnswer
        fields = ['studans_id','student_ansname', 'stud_answer']

