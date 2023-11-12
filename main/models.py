from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from froala_editor.fields import FroalaField
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django import forms
from django.core import validators
from django.db.models.signals import pre_save
from django.dispatch import receiver
# Create your models here.


class Student(models.Model):
    STATUS_CHOICES = [
        ('Approved', 'Approved'),
        ('Pending', 'Pending'),
        ('Declined', 'Declined'),
    ]

    status = models.CharField(
        max_length=10, 
        choices=STATUS_CHOICES, 
        default='Pending'  # Set the default status to 'Pending'
    )
   
    time_received = models.DateTimeField(null=True, blank=True)
    
    
    student_id = models.IntegerField(primary_key=True)
    registration_type = models.CharField(max_length=50, null=True)

    first_name = models.CharField(max_length=50, null=False)
    middle_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=100, null=False)

    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]

    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, null=True, blank=True)
    
    contact_number = models.CharField(max_length=11, null=True, blank=True)
    email = models.EmailField(max_length=100, null=True, blank=True)
    password = models.CharField(max_length=255, null=False)
    date_of_birth = models.DateField(null=True, blank=True)
    place_of_birth = models.CharField(max_length=100, null=True, blank=True)

    #Religion Selections
    RELIGION_CHOICES = [
        ('Roman Catholicism', 'Roman Catholicism'),
        ('Islam', 'Islam'),
        ('Protestant Christianity', 'Protestant Christianity'),
        ('Iglesia ni Cristo', 'Iglesia ni Cristo'),
        ('Lumad and Indigenous Beliefs', 'Lumad and Indigenous Beliefs'),
        ('Buddhism', 'Buddhism'),
        ('Taoism', 'Taoism')

    ]

    religion = models.CharField(max_length=100, choices=RELIGION_CHOICES, null=True, blank=True)

    CITIZENSHIP_CHOICES = [
    ('Filipino Citizen', 'Filipino Citizen'),
    ('Dual Citizen', 'Dual Citizen'),
    ('Former Filipino Citizen', 'Former Filipino Citizen'),
    ('Foreign Citizen', 'Foreign Citizen')
    ]

    citizenship = models.CharField(max_length=100, choices=CITIZENSHIP_CHOICES, null=True, blank=True)
    
    barangay = models.CharField(max_length=100, null=True, blank=True)
    
    #Senior High Track G11

    SENIOR_HIGH_TRACK_CHOICES = [
        ('ABM', 'Accountancy, Business and Management Strand'),
        ('STEM', 'Science, Technology, Engineering, and Mathematics Strand'),
        ('HUMMS', 'Humanities and Social Science Strand'),
        ('GAS', 'General Academic Strand'),
        ('TVL', 'Technical-Vocational-Livelihood Track'),
    ]

    senior_high_track = models.CharField(max_length=100, choices=SENIOR_HIGH_TRACK_CHOICES, null=True, blank=True)
    
    #Senior High Track G12

    SENIOR_HIGH_TRACKG12_CHOICES = [
        ('ABM', 'Accountancy, Business and Management Strand'),
        ('STEM', 'Science, Technology, Engineering, and Mathematics Strand'),
        ('HUMMS', 'Humanities and Social Science Strand'),
        ('GAS', 'General Academic Strand'),
        ('TVL', 'Technical-Vocational-Livelihood Track'),
    ]

    senior_high_track_g12 = models.CharField(max_length=100, choices=SENIOR_HIGH_TRACKG12_CHOICES, null=True, blank=True)
    
    #For educational background codes for models
    grade_school_name = models.CharField(max_length=100, null=True, blank=True)
    grade_school_address = models.CharField(max_length=200, null=True, blank=True)
    grade_school_year_graduated = models.IntegerField(null=True, blank=True)
    grade_school_awards_and_recognition = models.TextField(blank=True)

    junior_high_school_name = models.CharField(max_length=100, null=True, blank=True)
    junior_high_school_address = models.CharField(max_length=200, null=True, blank=True)
    junior_high_school_year_graduated = models.IntegerField(null=True, blank=True)
    junior_high_school_awards_and_recognition = models.TextField(blank=True)

    senior_high_school_name = models.CharField(max_length=100, null=True, blank=True)
    senior_high_school_address = models.CharField(max_length=200, null=True, blank=True)
    senior_high_school_year_graduated = models.IntegerField(null=True, blank=True)
    senior_high_school_awards_and_recognition = models.TextField(blank=True)

    vocational_school_name = models.CharField(max_length=100, null=True, blank=True)
    vocational_school_address = models.CharField(max_length=200, null=True, blank=True)
    vocational_school_year_graduated = models.IntegerField(null=True, blank=True)
    vocational_school_awards_and_recognition = models.TextField(blank=True)

    #For emergency models (for father only!)
    father_full_name = models.CharField(max_length=50, null=True, blank=True)
    father_contact_no = models.CharField(max_length=11, null=True, blank=True)
    father_home_add = models.CharField(max_length=100, null=True, blank=True)
    father_email_add = models.EmailField(max_length=100, null=True, blank=True)

    OCCUPATION_CHOICES = [
    ('Self-employed', 'Self-employed'),
    ('Unemployed', 'Unemployed'),
    ('Student', 'Student'),
    ('Retired', 'Retired'),
    ('Homemaker', 'Homemaker'),
    ('Other', 'Other'),
    ]

    occupation = models.CharField(max_length=20, choices=OCCUPATION_CHOICES, null=True, blank=True)

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

    income = models.CharField(max_length=15, choices=INCOME_CHOICES, null=True, blank=True)

    #For emergency models (for mother only!)
    mother_full_name = models.CharField(max_length=50, null=True, blank=True)
    mother_contact_no = models.CharField(max_length=11, null=True, blank=True)
    mother_home_add = models.CharField(max_length=100, null=True, blank=True)
    mother_email_add = models.EmailField(max_length=100, null=True, blank=True)

    MOTHOCCUPATION_CHOICES = [
    ('Employed', 'Employed'),
    ('Unemployed', 'Unemployed'),
    ('Self-employed', 'Self-employed'),
    ('Student', 'Student'),
    ('Retired', 'Retired'),
    ('Homemaker', 'Homemaker'),
    ('Other', 'Other'),
    ]

    moth_occupation = models.CharField(max_length=20, choices=MOTHOCCUPATION_CHOICES, null=True, blank=True)

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

    moth_income = models.CharField(max_length=15, choices=INCOME_CHOICES, null=True, blank=True)
    
    #For grades per subject
    gwa = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        default=75.00,
        validators=[
            MinValueValidator(75, "GWA must be at least 75."),
            MaxValueValidator(99, "GWA cannot exceed 99."),
        ]
    )

    def determine_department(self):
        if self.gwa >= 97:
            self.department = "BACHELOR OF SCIENCE IN COMPUTER SCIENCE (APPLICATION DEVELOPMENT ELECTIVE TRACK)"
        elif self.gwa >= 95:
            self.department = "BACHELOR OF SCIENCE IN INFORMATION TECHNOLOGY (INFORMATION AND NETWORK SECURITY ELECTIVE TRACK)"
        elif self.gwa >= 90:
            self.department = "BSCS MAJOR IN SOCIAL COMPUTING"
        elif self.gwa >= 80:
            self.department = "DIPLOMA IN APPLICATION DEVELOPMENT"
        else:
            self.department = "No recommended department based on GWA"

        self.save()

    #For grades per subject
    gwa_g12 = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        default=75.00,
        validators=[
            MinValueValidator(75, "GWA must be at least 75."),
            MaxValueValidator(99, "GWA cannot exceed 99."),
        ]
    )

    predicted_course = models.CharField(max_length=100, blank=True)

    oralcom = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        default=75.00,
        validators=[
            MinValueValidator(75, "GWA must be at least 75."),
            MaxValueValidator(99, "GWA cannot exceed 95."),
        ]

    )

    genmath = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        default=75.00,
        validators=[
            MinValueValidator(75, "GWA must be at least 75."),
            MaxValueValidator(99, "GWA cannot exceed 95."),
        ]
    )

    earthscie = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        default=75.00,
        validators=[
            MinValueValidator(75, "GWA must be at least 75."),
            MaxValueValidator(99, "GWA cannot exceed 95."),
        ]
    )

    probstats = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        default=75.00,
        validators=[
            MinValueValidator(75, "GWA must be at least 75."),
            MaxValueValidator(99, "GWA cannot exceed 95."),
        ]
    )

    CIVIL_STATUS_CHOICES = [
        ('Single', 'Single'),
        ('Married', 'Married'),
        ('Divorced', 'Divorced'),
        ('Widowed', 'Widowed'),
        ('Other', 'Other'),
    ]

    civil_status = models.CharField(max_length=10, choices=CIVIL_STATUS_CHOICES, null=True, blank=True)

    REGION_CHOICES = [
        ('Region I - Ilocos Region', 'Region I - Ilocos Region'),
        ('Region II - Cagayan Valley', 'Region II - Cagayan Valley'),
        ('Region III - Central Luzon', 'Region III - Central Luzon'),
        ('Region IV-A - Calabarzon', 'Region IV-A - Calabarzon'),
        ('MIMAROPA Region', 'MIMAROPA Region'),
        ('Region V - Bicol Region', 'Region V - Bicol Region'),
        ('Region VI - Western Visayas', 'Region VI - Western Visayas'),
        ('Region VII - Central Visayas', 'Region VII - Central Visayas'),
        ('Region VIII - Eastern Visayas', 'Region VIII - Eastern Visayas'),
        ('Region IX - Zamboanga Peninsula', 'Region IX - Zamboanga Peninsula'),
        ('Region X - Northern Mindanao', 'Region X - Northern Mindanao'),
        ('Region XI - Davao Region', 'Region XI - Davao Region'),
        ('Region XII - SOCCSKSARGEN', 'Region XII - SOCCSKSARGEN'),
        ('Region XIII - Caraga', 'Region XIII - Caraga'),
        ('NCR - National Capital Region', 'NCR - National Capital Region'),
        ('CAR - Cordillera Administrative Region', 'CAR - Cordillera Administrative Region'),
        ('BARMM - Bangsamoro Autonomous Region in Muslim Mindanao', 'BARMM - Bangsamoro Autonomous Region in Muslim Mindanao'),
    ]

    region = models.CharField(max_length=100, choices=REGION_CHOICES, null=True, blank=True)

    PROVINCE_CHOICE = [
        ('Abra', 'Abra'),
        ('Agusan del Norte', 'Agusan del Norte'),
        ('Agusan del Sur', 'Agusan del Sur'),
        ('Aklan', 'Aklan'),
        ('Albay', 'Albay'),
        ('Antique', 'Antique'),
        ('Apayao', 'Apayao'),
        ('Aurora', 'Aurora'),
        ('Basilan', 'Basilan'),
        ('Bataan', 'Bataan'),
        ('Batanes', 'Batanes'),
        ('Batangas', 'Batangas'),
        ('Benguet', 'Benguet'),
        ('Biliran', 'Biliran'),
        ('Bohol', 'Bohol'),
        ('Bukidnon', 'Bukidnon'),
        ('Bulacan', 'Bulacan'),
        ('Cagayan', 'Cagayan'),
        ('Camarines Norte', 'Camarines Norte'),
        ('Camarines Sur', 'Camarines Sur'),
        ('Camiguin', 'Camiguin'),
        ('Capiz', 'Capiz'),
        ('Catanduanes', 'Catanduanes'),
        ('Cavite', 'Cavite'),
        ('Cebu', 'Cebu'),
        ('Cotabato', 'Cotabato'),
        ('Davao de Oro (Compostela Valley)', 'Davao de Oro (Compostela Valley)'),
        ('Davao del Norte', 'Davao del Norte'),
        ('Davao del Sur', 'Davao del Sur'),
        ('Davao Occidental', 'Davao Occidental'),
        ('Davao Oriental', 'Davao Oriental'),
        ('Dinagat Islands', 'Dinagat Islands'),
        ('Eastern Samar', 'Eastern Samar'),
        ('Guimaras', 'Guimaras'),
        ('Ifugao', 'Ifugao'),
        ('Ilocos Norte', 'Ilocos Norte'),
        ('Ilocos Sur', 'Ilocos Sur'),
        ('Iloilo', 'Iloilo'),
        ('Isabela', 'Isabela'),
        ('Kalinga', 'Kalinga'),
        ('La Union', 'La Union'),
        ('Laguna', 'Laguna'),
        ('Lanao del Norte', 'Lanao del Norte'),
        ('Lanao del Sur', 'Lanao del Sur'),
        ('Leyte', 'Leyte'),
        ('Maguindanao del Norte', 'Maguindanao del Norte'),
        ('Maguindanao del Sur', 'Maguindanao del Sur'),
        ('Marinduque', 'Marinduque'),
        ('Masbate', 'Masbate'),
        ('Misamis Occidental', 'Misamis Occidental'),
        ('Misamis Oriental', 'Misamis Oriental'),
        ('Mountain Province', 'Mountain Province'),
        ('Negros Occidental', 'Negros Occidental'),
        ('Negros Oriental', 'Negros Oriental'),
        ('Northern Samar', 'Northern Samar'),
        ('Nueva Ecija', 'Nueva Ecija'),
        ('Nueva Vizcaya', 'Nueva Vizcaya'),
        ('Occidental Mindoro', 'Occidental Mindoro'),
        ('Oriental Mindoro', 'Oriental Mindoro'),
        ('Palawan', 'Palawan'),
        ('Pampanga', 'Pampanga'),
        ('Pangasinan', 'Pangasinan'),
        ('Quezon', 'Quezon'),
        ('Quirino', 'Quirino'),
        ('Rizal', 'Rizal'),
        ('Romblon', 'Romblon'),
        ('Samar', 'Samar'),
        ('Sarangani', 'Sarangani'),
        ('Siquijor', 'Siquijor'),
        ('Sorsogon', 'Sorsogon'),
        ('South Cotabato', 'South Cotabato'),
        ('Southern Leyte', 'Southern Leyte'),
        ('Sultan Kudarat', 'Sultan Kudarat'),
        ('Sulu', 'Sulu'),
        ('Surigao del Norte', 'Surigao del Norte'),
        ('Surigao del Sur', 'Surigao del Sur'),
        ('Tarlac', 'Tarlac'),
        ('Tawi Tawi', 'Tawi Tawi'),
        ('Zambales', 'Zambales'),
        ('Zamboanga del Norte', 'Zamboanga del Norte'),
        ('Zamboanga del Sur', 'Zamboanga del Sur'),
        ('Zamboanga Sibugay', 'Zamboanga Sibugay'),

    ]

    province = models.CharField(max_length=100, choices=PROVINCE_CHOICE, null=True, blank=True)

    CITY_CHOICE = [
        ('Caloocan', 'Caloocan'),
        ('Las Pinas', 'Las Piñas'),
        ('Makati', 'Makati'),
        ('Malabon', 'Malabon'),
        ('Mandaluyong', 'Mandaluyong'),
        ('Manila;', 'Manila'),
        ('Marikina', 'Marikina'),
        ('Muntinlupa', 'Muntinlupa'),
        ('Navotas', 'Navotas'),
        ('Paranaque', 'Parañaque'),
        ('Pasay', 'Pasay'),
        ('Pasig', 'Pasig'),
        ('Pateros', 'Pateros'),
        ('Quezon City', 'Quezon City'),
        ('San Juan', 'San Juan'),
        ('Taguig', 'Taguig'),
        ('Valenzuela', 'Valenzuela'),
        ('Batangas', 'Batangas'),
        ('Cavite', 'Cavite'),
        ('Laguna', 'Laguna'),
        ('Lucena', 'Lucena'),
        ('Quezon', 'Quezon'),
        ('Rizal', 'Rizal'),
        
    ]

    city = models.CharField(max_length=100, choices=CITY_CHOICE, null=True, blank=True)

    COURSE1_CHOICE = [
        ('Bachelor of Science in Information Technology (Information and Network Security Elective Track)', 'Bachelor of Science in Information Technology (Information and Network Security Elective Track)'),
        ('Bachelor of Science in Computer Science (Computational and Data Sciences Elective Track)', 'Bachelor of Science in Computer Science (Computational and Data Sciences Elective Track)'),
        ('Bachelor of Science in Computer Science (Application Development Elective Track)', 'Bachelor of Science in Computer Science (Application Development Elective Track)'),
        ('Bachelor of Science in Computer Science Major in Social Computing', 'Bachelor of Science in Computer Science Major in Social Computing'),
        ('Diploma in Application Development', 'Diploma in Application Development'),
        ('Diploma in Computer Network Administration', 'Diploma in Computer Network Administration'),
    
    ]

    course1 = models.CharField(max_length=100, choices=COURSE1_CHOICE, null=True, blank=True)

    COURSE2_CHOICE = [
        ('Bachelor of Science in Information Technology (Information and Network Security Elective Track)', 'Bachelor of Science in Information Technology (Information and Network Security Elective Track)'),
        ('Bachelor of Science in Computer Science (Computational and Data Sciences Elective Track)', 'Bachelor of Science in Computer Science (Computational and Data Sciences Elective Track)'),
        ('Bachelor of Science in Computer Science (Application Development Elective Track)', 'Bachelor of Science in Computer Science (Application Development Elective Track)'),
        ('Bachelor of Science in Computer Science Major in Social Computing', 'Bachelor of Science in Computer Science Major in Social Computing'),
        ('Diploma in Application Development', 'Diploma in Application Development'),
        ('Diploma in Computer Network Administration', 'Diploma in Computer Network Administration'),
    ]

    course2 = models.CharField(max_length=100, choices=COURSE1_CHOICE, null=True, blank=True)

    course = models.ManyToManyField(
        'Course', related_name='students', blank=True)
    
    department = models.ForeignKey(
        'Department', on_delete=models.CASCADE, null=True, blank=True, related_name='students')

    role = models.CharField(
        default="Student", max_length=100, null=False, blank=True)
    
    photo = models.ImageField(upload_to='profile_pics', blank=True, null=True)
    
    def delete(self, *args, **kwargs):
        if self.photo != 'profile_pics/default_student.png':
            self.photo.delete()
        super().delete(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Students'

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
        
    #def __str__(self):
        #return self.last_name


class Faculty(models.Model):
    faculty_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100, null=False)
    email = models.EmailField(max_length=100, null=True, blank=True)
    password = models.CharField(max_length=255, null=False)
    department = models.ForeignKey(
        'Department', on_delete=models.CASCADE, null=False, related_name='faculty')
    role = models.CharField(
        default="Faculty", max_length=100, null=False, blank=True)
    photo = models.ImageField(upload_to='profile_pics', blank=True,
                              null=False, default='profile_pics/default_faculty.png')

    def delete(self, *args, **kwargs):
        if self.photo != 'profile_pics/default_faculty.png':
            self.photo.delete()
        super().delete(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Faculty'

    def __str__(self):
        return self.name


class Department(models.Model):
    department_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100, null=False)
    description = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Departments'

    def __str__(self):
        return self.name

    def student_count(self):
        return self.students.count()

    def faculty_count(self):
        return self.faculty.count()

    def course_count(self):
        return self.courses.count()


class Course(models.Model):
    code = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255, null=False, unique=True)
    department = models.ForeignKey(
        Department, on_delete=models.CASCADE, null=False, related_name='courses')
    faculty = models.ForeignKey(
        Faculty, on_delete=models.SET_NULL, null=True, blank=True)
    studentKey = models.IntegerField(null=False, unique=True)
    facultyKey = models.IntegerField(null=False, unique=True)

    class Meta:
        unique_together = ('code', 'department', 'name')
        verbose_name_plural = "Courses"

    def __str__(self):
        return self.name


class Announcement(models.Model):
    course_code = models.ForeignKey(Course, on_delete=models.CASCADE, null=False)
    datetime = models.DateTimeField(auto_now_add=True, null=False)
    
    description = FroalaField()

    class Meta:
        verbose_name_plural = "Announcements for Program Courses"
        ordering = ['-datetime']

    def __str__(self):
        return self.datetime.strftime("%d-%b-%y, %I:%M %p")

    def post_date(self):
        return self.datetime.strftime("%d-%b-%y, %I:%M %p")



class Assignment(models.Model):
    course_code = models.ForeignKey(
        Course, on_delete=models.CASCADE, null=False)
    title = models.CharField(max_length=255, null=False)
    description = FroalaField()
    datetime = models.DateTimeField(auto_now_add=True, null=False)
    deadline = models.DateTimeField(null=False)
    file = models.FileField(upload_to='assignments/', null=True, blank=True)
    marks = models.DecimalField(max_digits=6, decimal_places=2, null=False)

    class Meta:
        verbose_name_plural = "Course Materials"
        ordering = ['-datetime']

    def __str__(self):
        return self.title
        
    def delete(self, *args, **kwargs):
        self.file.delete()
        super().delete(*args, **kwargs)
    
    def post_date(self):
        return self.datetime.strftime("%d-%b-%y, %I:%M %p")
    
    def due_date(self):
        return self.deadline.strftime("%d-%b-%y, %I:%M %p")


class Submission(models.Model):
    assignment = models.ForeignKey(
        Assignment, on_delete=models.CASCADE, null=False)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=False)
    file = models.FileField(upload_to='submissions/', null=True,)
    datetime = models.DateTimeField(auto_now_add=True, null=False)
    marks = models.DecimalField(
        max_digits=6, decimal_places=2, null=True, blank=True)
    status = models.CharField(max_length=100, null=True, blank=True)

    def file_name(self):
        return self.file.name.split('/')[-1]

    def time_difference(self):
        difference = self.assignment.deadline - self.datetime
        days = difference.days
        hours = difference.seconds//3600
        minutes = (difference.seconds//60) % 60
        seconds = difference.seconds % 60

        if days == 0:
            if hours == 0:
                if minutes == 0:
                    return str(seconds) + " seconds"
                else:
                    return str(minutes) + " minutes " + str(seconds) + " seconds"
            else:
                return str(hours) + " hours " + str(minutes) + " minutes " + str(seconds) + " seconds"
        else:
            return str(days) + " days " + str(hours) + " hours " + str(minutes) + " minutes " + str(seconds) + " seconds"

    def submission_date(self):
        return self.datetime.strftime("%d-%b-%y, %I:%M %p")

    def delete(self, *args, **kwargs):
        self.file.delete()
        super().delete(*args, **kwargs)

    def __str__(self):
        return self.student.name + " - " + self.assignment.title

    class Meta:
        unique_together = ('assignment', 'student')
        verbose_name_plural = "Submissions"
        ordering = ['datetime']


class Material(models.Model):
    course_code = models.ForeignKey(
        Course, on_delete=models.CASCADE, null=False)
    description = models.TextField(max_length=2000, null=False)
    datetime = models.DateTimeField(auto_now_add=True, null=False)
    file = models.FileField(upload_to='materials/', null=True, blank=True)

    class Meta:
        verbose_name_plural = "Materials"
        ordering = ['-datetime']

    def __str__(self):
        return self.title

    def delete(self, *args, **kwargs):
        self.file.delete()
        super().delete(*args, **kwargs)

    def post_date(self):
        return self.datetime.strftime("%d-%b-%y, %I:%M %p")

class AdmissionRequirement(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return self.title

class Feedback(models.Model):
    student_id = models.PositiveIntegerField()
    student_name = models.CharField(max_length=100)
    department = models.CharField(
        max_length=100,
        choices=[
            ('BSIT (Information and Network Security Elective Track)', 'BSIT (Information and Network Security Elective Track)'),
            ('BSCS (Computational and Data Sciences Elective Track)', 'BSCS (Computational and Data Sciences Elective Track)'),
            ('BSCS (Application Development Elective Track)', 'BSCS (Application Development Elective Track)'),
            ('BSCS Major in Social Computing', 'BSCS Major in Social Computing'),
            ('Diploma in Application Development', 'Diploma in Application Development'),
            ('Diploma in Computer Network Administration', 'Diploma in Computer Network Administration'),
        ]
    )
    feedback_messages = models.TextField()

    def __str__(self):
        return f"Feedback for {self.student_name}"

class StudentAnswer(models.Model):
    studans_id = models.PositiveIntegerField()
    student_ansname = models.CharField(max_length=100)
    stud_answer = models.TextField() 

    def __str__(self):
        return f"Answer for {self.student_ansname}"

