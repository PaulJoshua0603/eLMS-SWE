import datetime
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from .models import Student, Course, Announcement, Assignment, Material, Faculty, Department, AdmissionRequirement, Feedback, StudentAnswer
from django.utils import timezone
# Add Submission if necessary
from django.template.defaulttags import register
from django.db.models import Count, Q
from django.http import HttpResponseRedirect
#Forms.py codes
from .forms import AnnouncementForm, AssignmentForm, MaterialForm, RegistrationForm, FeedbackForm, StudentAnswerForm
from django import forms
from django.core import validators
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.http import JsonResponse
#for pdf imports
from reportlab.lib.pagesizes import landscape, letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from io import BytesIO
from django.http import HttpResponse, HttpResponseBadRequest
from reportlab.lib import colors
from reportlab.platypus import Paragraph
from reportlab.platypus import Spacer
from reportlab.lib.styles import getSampleStyleSheet
#picture
from django.core.files.storage import FileSystemStorage
#Algorithm
import joblib
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
#
import pickle
import pandas as pd

# Load model
with open('random_forest_model.pkl', 'rb') as model_file:
    loaded_model = pickle.load(model_file)


class LoginForm(forms.Form):
    id = forms.CharField(label='ID', max_length=10, validators=[
                         validators.RegexValidator(r'^\d+$', 'Please enter a valid number.')])
    password = forms.CharField(widget=forms.PasswordInput)


def is_student_authorised(request, code):
    course = Course.objects.get(code=code)
    if request.session.get('student_id') and course in Student.objects.get(student_id=request.session['student_id']).course.all():
        return True
    else:
        return False


def is_faculty_authorised(request, code):
    if request.session.get('faculty_id') and code in Course.objects.filter(faculty_id=request.session['faculty_id']).values_list('code', flat=True):
        return True
    else:
        return False


# Custom Login page for student and faculty
def std_login(request):
    error_messages = []

    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            id = form.cleaned_data['id']
            password = form.cleaned_data['password']

            if Student.objects.filter(student_id=id, password=password).exists():
                request.session['student_id'] = id
                return redirect('home') #change later in home page directly
            elif Faculty.objects.filter(faculty_id=id, password=password).exists():
                request.session['faculty_id'] = id
                return redirect('facultyCourses')
            else:
                error_messages.append('Invalid login credentials.')
        else:
            error_messages.append('Invalid form data.')
    else:
        form = LoginForm()

    if 'student_id' in request.session:
        return redirect('/my/')
    elif 'faculty_id' in request.session:
        return redirect('/facultyCourses/')

    context = {'form': form, 'error_messages': error_messages}
    return render(request, 'login_page.html', context)

# Registration Page
def register_user(request):
    error_messages = []
    success_message = ""

    if request.method == 'POST':
        form = RegistrationForm(request.POST, request.FILES)
        print("Checking Forms")
        if form.is_valid():
            print("Form is valid")
            time_received = form.cleaned_data['time_received']

            student_id = form.cleaned_data['student_id']
            registration_type = form.cleaned_data['registration_type']

            password = form.cleaned_data['password']
            confirm_password = form.cleaned_data['confirm_password']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            first_name = form.cleaned_data['first_name']
            middle_name = form.cleaned_data['middle_name']
            date_of_birth = form.cleaned_data['date_of_birth']
            place_of_birth = form.cleaned_data['place_of_birth']
            gender = form.cleaned_data['gender']
            religion = form.cleaned_data['religion']
            civil_status=form.cleaned_data['civil_status']
            citizenship=form.cleaned_data['citizenship']
            contact_number=form.cleaned_data['contact_number']
            region=form.cleaned_data['region']
            province=form.cleaned_data['province']
            city=form.cleaned_data['city']
            barangay=form.cleaned_data['barangay']

            photo = form.cleaned_data['photo']

            course1=form.cleaned_data['course1']
            course2=form.cleaned_data['course2']

            senior_high_track = form.cleaned_data['senior_high_track']
            senior_high_track_g12=form.cleaned_data['senior_high_track_g12']

            gwa = form.cleaned_data['gwa']
            gwa_g12 = form.cleaned_data['gwa_g12']

            
            oralcom = form.cleaned_data['oralcom']
            genmath = form.cleaned_data['genmath']
            earthscie = form.cleaned_data['earthscie']
            probstats = form.cleaned_data['probstats']

            #For educational background in views.py
            grade_school_name = form.cleaned_data['grade_school_name']
            grade_school_address = form.cleaned_data['grade_school_address']
            grade_school_year_graduated = form.cleaned_data['grade_school_year_graduated']
            grade_school_awards_and_recognition = form.cleaned_data['grade_school_awards_and_recognition']
            
            junior_high_school_name = form.cleaned_data['junior_high_school_name']
            junior_high_school_address = form.cleaned_data['junior_high_school_address']
            junior_high_school_year_graduated = form.cleaned_data['junior_high_school_year_graduated']
            junior_high_school_awards_and_recognition = form.cleaned_data['junior_high_school_awards_and_recognition']

            senior_high_school_name = form.cleaned_data['senior_high_school_name']
            senior_high_school_address = form.cleaned_data['senior_high_school_address']
            senior_high_school_year_graduated = form.cleaned_data['senior_high_school_year_graduated']
            senior_high_school_awards_and_recognition = form.cleaned_data['senior_high_school_awards_and_recognition']
            
            vocational_school_name = form.cleaned_data['vocational_school_name']
            vocational_school_address = form.cleaned_data['vocational_school_address']
            vocational_school_year_graduated = form.cleaned_data['vocational_school_year_graduated']
            vocational_school_awards_and_recognition = form.cleaned_data['vocational_school_awards_and_recognition']
            
            #For emergency views (For father only!)
            father_full_name = form.cleaned_data['father_full_name']
            father_contact_no = form.cleaned_data['father_contact_no']
            occupation = form.cleaned_data['occupation']
            father_home_add = form.cleaned_data['father_home_add']
            father_email_add = form.cleaned_data['father_email_add']
            income = form.cleaned_data['income']

            #For emergency view (for mother only!)
            mother_full_name = form.cleaned_data['mother_full_name']
            mother_contact_no = form.cleaned_data['mother_contact_no']
            moth_occupation = form.cleaned_data['moth_occupation']
            mother_home_add = form.cleaned_data['mother_home_add']
            mother_email_add = form.cleaned_data['mother_email_add']
            moth_income = form.cleaned_data['moth_income']

            

            # If validation is successful, you can create a new student object
            student = Student(
                time_received=time_received,

                registration_type=registration_type,
                student_id=student_id,

                first_name=first_name,
                middle_name=middle_name,
                last_name=last_name,
                date_of_birth=date_of_birth,
                place_of_birth=place_of_birth,
                gender=gender,
                religion=religion,
                civil_status=civil_status,
                citizenship=citizenship,
                contact_number=contact_number,
                email=email,
                password=password,
                region=region,
                province=province,
                city=city,
                barangay=barangay,
                course1=course1,
                course2=course2,

                photo=photo,

                senior_high_track = senior_high_track,
                senior_high_track_g12=senior_high_track_g12,

                gwa=gwa,
                gwa_g12=gwa_g12,

                oralcom=oralcom,
                genmath=genmath,
                earthscie=earthscie,
                probstats=probstats,

                father_full_name=father_full_name,
                father_contact_no=father_contact_no,
                occupation=occupation,
                father_home_add=father_home_add,
                father_email_add=father_email_add,
                income = income,
                mother_full_name=mother_full_name,
                mother_contact_no=mother_contact_no,
                moth_occupation=moth_occupation,
                mother_home_add=mother_home_add,
                mother_email_add=mother_email_add,
                moth_income=moth_income,

                #For educational background in views.py
                grade_school_name=grade_school_name,
                grade_school_address=grade_school_address,
                grade_school_year_graduated=grade_school_year_graduated,
                grade_school_awards_and_recognition=grade_school_awards_and_recognition,

                junior_high_school_name=junior_high_school_name,
                junior_high_school_address=junior_high_school_address,
                junior_high_school_year_graduated=junior_high_school_year_graduated,
                junior_high_school_awards_and_recognition=junior_high_school_awards_and_recognition,

                senior_high_school_name = senior_high_school_name,
                senior_high_school_address = senior_high_school_address,
                senior_high_school_year_graduated = senior_high_school_year_graduated,
                senior_high_school_awards_and_recognition = senior_high_school_awards_and_recognition,

                vocational_school_name = vocational_school_name,
                vocational_school_address = vocational_school_address,
                vocational_school_year_graduated = vocational_school_year_graduated,
                vocational_school_awards_and_recognition = vocational_school_awards_and_recognition

            )
            student.time_received = timezone.now()
            student.save()

            # Log in the newly registered student
            user = authenticate(request, username=student_id, password=password)
            if user:
                login(request, user)

            print("Registration Success")
            messages.success(request, "Registration Successful!")
            success_message = "Registration Successfully!"
            return render(request, 'register_user.html', {'success_message': success_message})
        else:
            print("Invalid Form Data")
            print (form)
            error_messages.append('Invalid form data.')
    else:
        print("Invalid Registration")
        form = RegistrationForm()

    context = {'form': form, 'success_message': success_message}
    return render(request, 'register_user.html', context)
    
# End of coding


# Clears the session on logout
def std_logout(request):
    request.session.flush()
    return redirect('std_login')


# Display all courses (student view)
def myCourses(request):
    try:
        if request.session.get('student_id'):
            student = Student.objects.get(
                student_id=request.session['student_id'])
            courses = student.course.all()
            faculty = student.course.all().values_list('faculty_id', flat=True)

              # sample data
            new_data = pd.DataFrame({
            'EnglishOverall': [student.oralcom],
            'MathematicsOverall': [student.genmath],
            'ScienceOverall': [student.earthscie],
            'CRSOverall': [student.gwa_g12]
            })

            predictions = loaded_model.predict(new_data)

            context = {
                'courses': courses,
                'student': student,
                'faculty': faculty,
                'predictions': predictions
            }
              
            # Display the predictions
            #print("Test Predictions:")
            #print(predictions)

            return render(request, 'main/myCourses.html', context)
        else:
            return redirect('std_login')
    except:
        return render(request, 'error.html')


# Display all courses (faculty view)
def facultyCourses(request):
    try:
        if request.session['faculty_id']:
            faculty = Faculty.objects.get(
                faculty_id=request.session['faculty_id'])
            courses = Course.objects.filter(
                faculty_id=request.session['faculty_id'])
            # Student count of each course to show on the faculty page
            studentCount = Course.objects.all().annotate(student_count=Count('students'))

            studentCountDict = {}

            for course in studentCount:
                studentCountDict[course.code] = course.student_count

            @register.filter
            def get_item(dictionary, course_code):
                return dictionary.get(course_code)

            context = {
                'courses': courses,
                'faculty': faculty,
                'studentCount': studentCountDict
            }

            return render(request, 'main/facultyCourses.html', context)

        else:
            return redirect('std_login')
    except:

        return redirect('std_login')


# Particular course page (student view)
def course_page(request, code):
    try:
        course = Course.objects.get(code=code)
        if is_student_authorised(request, code):
            try:
                announcements = Announcement.objects.filter(course_code=course)
                assignments = Assignment.objects.filter(
                    course_code=course.code)
                materials = Material.objects.filter(course_code=course.code)

            except:
                announcements = None
                assignments = None
                materials = None

            context = {
                'course': course,
                'announcements': announcements,
                'assignments': assignments[:3],
                'materials': materials,
                'student': Student.objects.get(student_id=request.session['student_id'])
            }

            return render(request, 'main/course.html', context)

        else:
            return redirect('std_login')
    except:
        return render(request, 'error.html')


# Particular course page (faculty view)
def course_page_faculty(request, code):
    course = Course.objects.get(code=code)
    if request.session.get('faculty_id'):
        try:
            announcements = Announcement.objects.filter(course_code=course)
            assignments = Assignment.objects.filter(
                course_code=course.code)
            materials = Material.objects.filter(course_code=course.code)
            studentCount = Student.objects.filter(course=course).count()

        except:
            announcements = None
            assignments = None
            materials = None

        context = {
            'course': course,
            'announcements': announcements,
            'assignments': assignments[:3],
            'materials': materials,
            'faculty': Faculty.objects.get(faculty_id=request.session['faculty_id']),
            'studentCount': studentCount
        }

        return render(request, 'main/faculty_course.html', context)
    else:
        return redirect('std_login')


def error(request):
    return render(request, 'error.html')


# Display user profile(student & faculty)
def profile(request, id):
    try:
        if request.session['student_id'] == id:
            student = Student.objects.get(student_id=id)
            return render(request, 'main/profile.html', {'student': student})
        else:
            return redirect('std_login')
    except:
        try:
            if request.session['faculty_id'] == id:
                faculty = Faculty.objects.get(faculty_id=id)
                return render(request, 'main/faculty_profile.html', {'faculty': faculty})
            else:
                return redirect('std_login')
        except:
            return render(request, 'error.html')
# End of coding

# Start coding for announcement
def addAnnouncement(request, code):
    if is_faculty_authorised(request, code):
        if request.method == 'POST':
            form = AnnouncementForm(request.POST)
            form.instance.course_code = Course.objects.get(code=code)
            if form.is_valid():
                form.save()
                messages.success(
                    request, 'Announcement added successfully.')
                return redirect('/faculty/' + str(code))
        else:
            form = AnnouncementForm()
        return render(request, 'main/announcement.html', {'course': Course.objects.get(code=code), 'faculty': Faculty.objects.get(faculty_id=request.session['faculty_id']), 'form': form})
    else:
        return redirect('std_login')


def deleteAnnouncement(request, code, id):
    if is_faculty_authorised(request, code):
        try:
            announcement = Announcement.objects.get(course_code=code, id=id)
            announcement.delete()
            messages.warning(request, 'Announcement deleted successfully.')
            return redirect('/faculty/' + str(code))
        except:
            return redirect('/faculty/' + str(code))
    else:
        return redirect('std_login')


def editAnnouncement(request, code, id):
    if is_faculty_authorised(request, code):
        announcement = Announcement.objects.get(course_code_id=code, id=id)
        form = AnnouncementForm(instance=announcement)
        context = {
            'announcement': announcement,
            'course': Course.objects.get(code=code),
            'faculty': Faculty.objects.get(faculty_id=request.session['faculty_id']),
            'form': form
        }
        return render(request, 'main/update-announcement.html', context)
    else:
        return redirect('std_login')


def updateAnnouncement(request, code, id):
    if is_faculty_authorised(request, code):
        try:
            announcement = Announcement.objects.get(course_code_id=code, id=id)
            
            form = AnnouncementForm(request.POST, instance=announcement)
            if form.is_valid():
                form.save()
                messages.info(request, 'Announcement updated successfully.')
                return redirect('/faculty/' + str(code))
        except:
            return redirect('/faculty/' + str(code))

    else:
        return redirect('std_login')

#End of coding


def addAssignment(request, code):
    if is_faculty_authorised(request, code):
        if request.method == 'POST':
            form = AssignmentForm(request.POST, request.FILES)
            form.instance.course_code = Course.objects.get(code=code)
            if form.is_valid():
                form.save()
                messages.success(request, 'Assignment added successfully.')
                return redirect('/faculty/' + str(code))
        else:
            form = AssignmentForm()
        return render(request, 'main/assignment.html', {'course': Course.objects.get(code=code), 'faculty': Faculty.objects.get(faculty_id=request.session['faculty_id']), 'form': form})
    else:
        return redirect('std_login')


def assignmentPage(request, code, id):
    course = Course.objects.get(code=code)
    if is_student_authorised(request, code):
        assignment = Assignment.objects.get(course_code=course.code, id=id)
        try:

            submission = Submission.objects.get(assignment=assignment, student=Student.objects.get(
                student_id=request.session['student_id']))

            context = {
                'assignment': assignment,
                'course': course,
                'submission': submission,
                'time': datetime.datetime.now(),
                'student': Student.objects.get(student_id=request.session['student_id']),
                'courses': Student.objects.get(student_id=request.session['student_id']).course.all()
            }

            return render(request, 'main/assignment-portal.html', context)

        except:
            submission = None

        context = {
            'assignment': assignment,
            'course': course,
            'submission': submission,
            'time': datetime.datetime.now(),
            'student': Student.objects.get(student_id=request.session['student_id']),
            'courses': Student.objects.get(student_id=request.session['student_id']).course.all()
        }

        return render(request, 'main/assignment-portal.html', context)
    else:

        return redirect('std_login')


def allAssignments(request, code):
    if is_faculty_authorised(request, code):
        course = Course.objects.get(code=code)
        assignments = Assignment.objects.filter(course_code=course)
        studentCount = Student.objects.filter(course=course).count()

        context = {
            'assignments': assignments,
            'course': course,
            'faculty': Faculty.objects.get(faculty_id=request.session['faculty_id']),
            'studentCount': studentCount

        }
        return render(request, 'main/all-assignments.html', context)
    else:
        return redirect('std_login')


def allAssignmentsSTD(request, code):
    if is_student_authorised(request, code):
        course = Course.objects.get(code=code)
        assignments = Assignment.objects.filter(course_code=course)
        context = {
            'assignments': assignments,
            'course': course,
            'student': Student.objects.get(student_id=request.session['student_id']),

        }
        return render(request, 'main/all-assignments-std.html', context)
    else:
        return redirect('std_login')


def addSubmission(request, code, id):
    try:
        course = Course.objects.get(code=code)
        if is_student_authorised(request, code):
            # check if assignment is open
            assignment = Assignment.objects.get(course_code=course.code, id=id)
            if assignment.deadline < datetime.datetime.now():

                return redirect('/assignment/' + str(code) + '/' + str(id))

            if request.method == 'POST' and request.FILES['file']:
                assignment = Assignment.objects.get(
                    course_code=course.code, id=id)
                submission = Submission(assignment=assignment, student=Student.objects.get(
                    student_id=request.session['student_id']), file=request.FILES['file'],)
                submission.status = 'Submitted'
                submission.save()
                return HttpResponseRedirect(request.path_info)
            else:
                assignment = Assignment.objects.get(
                    course_code=course.code, id=id)
                submission = Submission.objects.get(assignment=assignment, student=Student.objects.get(
                    student_id=request.session['student_id']))
                context = {
                    'assignment': assignment,
                    'course': course,
                    'submission': submission,
                    'time': datetime.datetime.now(),
                    'student': Student.objects.get(student_id=request.session['student_id']),
                    'courses': Student.objects.get(student_id=request.session['student_id']).course.all()
                }

                return render(request, 'main/assignment-portal.html', context)
        else:
            return redirect('std_login')
    except:
        return HttpResponseRedirect(request.path_info)


def viewSubmission(request, code, id):
    course = Course.objects.get(code=code)
    if is_faculty_authorised(request, code):
        try:
            assignment = Assignment.objects.get(course_code_id=code, id=id)
            submissions = Submission.objects.filter(
                assignment_id=assignment.id)

            context = {
                'course': course,
                'submissions': submissions,
                'assignment': assignment,
                'totalStudents': len(Student.objects.filter(course=course)),
                'faculty': Faculty.objects.get(faculty_id=request.session['faculty_id']),
                'courses': Course.objects.filter(faculty_id=request.session['faculty_id'])
            }

            return render(request, 'main/assignment-view.html', context)

        except:
            return redirect('/faculty/' + str(code))
    else:
        return redirect('std_login')


def gradeSubmission(request, code, id, sub_id):
    try:
        course = Course.objects.get(code=code)
        if is_faculty_authorised(request, code):
            if request.method == 'POST':
                assignment = Assignment.objects.get(course_code_id=code, id=id)
                submissions = Submission.objects.filter(
                    assignment_id=assignment.id)
                submission = Submission.objects.get(
                    assignment_id=id, id=sub_id)
                submission.marks = request.POST['marks']
                if request.POST['marks'] == 0:
                    submission.marks = 0
                submission.save()
                return HttpResponseRedirect(request.path_info)
            else:
                assignment = Assignment.objects.get(course_code_id=code, id=id)
                submissions = Submission.objects.filter(
                    assignment_id=assignment.id)
                submission = Submission.objects.get(
                    assignment_id=id, id=sub_id)

                context = {
                    'course': course,
                    'submissions': submissions,
                    'assignment': assignment,
                    'totalStudents': len(Student.objects.filter(course=course)),
                    'faculty': Faculty.objects.get(faculty_id=request.session['faculty_id']),
                    'courses': Course.objects.filter(faculty_id=request.session['faculty_id'])
                }

                return render(request, 'main/assignment-view.html', context)

        else:
            return redirect('std_login')
    except:
        return redirect('/error/')


def addCourseMaterial(request, code):
    if is_faculty_authorised(request, code):
        if request.method == 'POST':
            form = MaterialForm(request.POST, request.FILES)
            form.instance.course_code = Course.objects.get(code=code)
            if form.is_valid():
                form.save()
                messages.success(request, 'New course material added')
                return redirect('/faculty/' + str(code))
            else:
                return render(request, 'main/course-material.html', {'course': Course.objects.get(code=code), 'faculty': Faculty.objects.get(faculty_id=request.session['faculty_id']), 'form': form})
        else:
            form = MaterialForm()
            return render(request, 'main/course-material.html', {'course': Course.objects.get(code=code), 'faculty': Faculty.objects.get(faculty_id=request.session['faculty_id']), 'form': form})
    else:
        return redirect('std_login')


def deleteCourseMaterial(request, code, id):
    if is_faculty_authorised(request, code):
        course = Course.objects.get(code=code)
        course_material = Material.objects.get(course_code=course, id=id)
        course_material.delete()
        messages.warning(request, 'Course material deleted')
        return redirect('/faculty/' + str(code))
    else:
        return redirect('std_login')


def courses(request):
    if request.session.get('student_id') or request.session.get('faculty_id'):

        courses = Course.objects.all()
        if request.session.get('student_id'):
            student = Student.objects.get(
                student_id=request.session['student_id'])
        else:
            student = None
        if request.session.get('faculty_id'):
            faculty = Faculty.objects.get(
                faculty_id=request.session['faculty_id'])
        else:
            faculty = None

        enrolled = student.course.all() if student else None
        accessed = Course.objects.filter(
            faculty_id=faculty.faculty_id) if faculty else None

        context = {
            'faculty': faculty,
            'courses': courses,
            'student': student,
            'enrolled': enrolled,
            'accessed': accessed
        }

        return render(request, 'main/all-courses.html', context)

    else:
        return redirect('std_login')


def departments(request):
    if request.session.get('student_id') or request.session.get('faculty_id'):
        departments = Department.objects.all()
        if request.session.get('student_id'):
            student = Student.objects.get(
                student_id=request.session['student_id'])
        else:
            student = None
        if request.session.get('faculty_id'):
            faculty = Faculty.objects.get(
                faculty_id=request.session['faculty_id'])
        else:
            faculty = None
        context = {
            'faculty': faculty,
            'student': student,
            'deps': departments,
        }

        return render(request, 'main/departments.html', context)

    else:
        return redirect('std_login')


def access(request, code):
    if request.session.get('student_id'):
        course = Course.objects.get(code=code)
        student = Student.objects.get(student_id=request.session['student_id'])
        if request.method == 'POST':
            if (request.POST['key']) == str(course.studentKey):
                student.course.add(course)
                student.save()
                return redirect('/my/')
            else:
                messages.error(request, 'Invalid key')
                return HttpResponseRedirect(request.path_info)
        else:
            return render(request, 'main/access.html', {'course': course, 'student': student})

    else:
        return redirect('std_login')


def search(request):
    if request.session.get('student_id') or request.session.get('faculty_id'):
        if request.method == 'GET' and request.GET['q']:
            q = request.GET['q']
            courses = Course.objects.filter(Q(code__icontains=q) | Q(
                name__icontains=q) | Q(faculty__name__icontains=q))

            if request.session.get('student_id'):
                student = Student.objects.get(
                    student_id=request.session['student_id'])
            else:
                student = None
            if request.session.get('faculty_id'):
                faculty = Faculty.objects.get(
                    faculty_id=request.session['faculty_id'])
            else:
                faculty = None
            enrolled = student.course.all() if student else None
            accessed = Course.objects.filter(
                faculty_id=faculty.faculty_id) if faculty else None

            context = {
                'courses': courses,
                'faculty': faculty,
                'student': student,
                'enrolled': enrolled,
                'accessed': accessed,
                'q': q
            }
            return render(request, 'main/search.html', context)
        else:
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        return redirect('std_login')


def changePasswordPrompt(request):
    if request.session.get('student_id'):
        student = Student.objects.get(student_id=request.session['student_id'])
        return render(request, 'main/changePassword.html', {'student': student})
    elif request.session.get('faculty_id'):
        faculty = Faculty.objects.get(faculty_id=request.session['faculty_id'])
        return render(request, 'main/changePasswordFaculty.html', {'faculty': faculty})
    else:
        return redirect('std_login')


def changePhotoPrompt(request):
    if request.session.get('student_id'):
        student = Student.objects.get(student_id=request.session['student_id'])
        return render(request, 'main/changePhoto.html', {'student': student})
    elif request.session.get('faculty_id'):
        faculty = Faculty.objects.get(faculty_id=request.session['faculty_id'])
        return render(request, 'main/changePhotoFaculty.html', {'faculty': faculty})
    else:
        return redirect('std_login')


def changePassword(request):
    if request.session.get('student_id'):
        student = Student.objects.get(student_id=request.session['student_id'])
        if request.method == 'POST':
            if student.password == request.POST['oldPassword']:
                # New and confirm password check is done in the client side
                student.password = request.POST['newPassword']
                student.save()
                messages.success(request, 'Password was changed successfully')
                return redirect('student_profile', id=student.student_id)  # Redirect to student profile with success message
            else:
                messages.error(request, 'Password is incorrect. Please try again')
                return redirect('changePassword')
        else:
            return render(request, 'main/changePassword.html', {'student': student})
    else:
        return redirect('std_login')


def changePasswordFaculty(request):
    if request.session.get('faculty_id'):
        faculty = Faculty.objects.get(
            faculty_id=request.session['faculty_id'])
        if request.method == 'POST':
            if faculty.password == request.POST['oldPassword']:
                # New and confirm password check is done in the client side
                faculty.password = request.POST['newPassword']
                faculty.save()
                messages.success(request, 'Password was changed successfully')
                return redirect('/facultyProfile/' + str(faculty.faculty_id))
            else:
                print('error')
                messages.error(
                    request, 'Password is incorrect. Please try again')
                return redirect('/changePasswordFaculty/')
        else:
            print(faculty)
            return render(request, 'main/changePasswordFaculty.html', {'faculty': faculty})
    else:
        return redirect('std_login')


def changePhoto(request):
    if request.session.get('student_id'):
        student = Student.objects.get(student_id=request.session['student_id'])
        if request.method == 'POST':
            if request.FILES['photo']:
                student.photo = request.FILES['photo']
                student.save()
                messages.success(request, 'Profile picture was changed successfully')
                return redirect('student_profile', id=student.student_id) 
            else:
                messages.error(
                    request, 'Please select a photo')
                return redirect('/changePhoto/')
        else:
            return render(request, 'main/change_photo.html', {'student': student})  # Render the change photo form
    else:
        return redirect('std_login')


def changePhotoFaculty(request):
    if request.session.get('faculty_id'):
        faculty = Faculty.objects.get(
            faculty_id=request.session['faculty_id'])
        if request.method == 'POST':
            if request.FILES['photo']:
                faculty.photo = request.FILES['photo']
                faculty.save()
                messages.success(request, 'Photo was changed successfully')
                return redirect('/facultyProfile/' + str(faculty.faculty_id))
            else:
                messages.error(
                    request, 'Please select a photo')
                return redirect('/changePhotoFaculty/')
        else:
            return render(request, 'main/changePhotoFaculty.html', {'faculty': faculty})
    else:
        return redirect('std_login')


def guestStudent(request):
    request.session.flush()
    try:
        student = Student.objects.get(name='Guest Student')
        request.session['student_id'] = str(student.student_id)
        return redirect('myCourses')
    except:
        return redirect('std_login')


def guestFaculty(request):
    request.session.flush()
    try:
        faculty = Faculty.objects.get(name='Guest Faculty')
        request.session['faculty_id'] = str(faculty.faculty_id)
        return redirect('facultyCourses')
    except:
        return redirect('std_login')

def admission_index(request):
    admission_requirements = AdmissionRequirement.objects.all()
    return render(request, 'admission_index.html', {'admission_requirements': admission_requirements})

def notifications(request):
    context = {}
    return render(request, 'notifications.html', context)

def notifications(request):
    students = Student.objects.all()  # Query all student records from the database
    context = {'students': students}
    return render(request, 'notifications.html', context)
    
def student_profile(request, id):
    if 'student_id' in request.session and str(request.session['student_id']) == id:
        student = Student.objects.get(student_id=id)
        return render(request, 'student_profile.html', {'student': student})
    else:
        return redirect('std_login')

#Home Page
def home(request):
    return render(request, 'home.html')

def home(request):
    # Retrieve the student object if the user is logged in (you need to implement your authentication logic)
    student = None
    if 'student_id' in request.session:
        student_id = request.session['student_id']
        student = Student.objects.get(student_id=student_id)

    return render(request, 'home.html', {'student': student})

# For PDF Code views.py
def generate_pdf(request):
    students = Student.objects.all()
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="student_applications.pdf"'

    buffer = BytesIO()
    
    # Specify the landscape orientation
    doc = SimpleDocTemplate(buffer, pagesize=landscape(letter))

    elements = []

    styles = getSampleStyleSheet()
    styleN = styles['Normal']

    data = []
    data.append(["Student Name", "Email", "Program Course", "Time Registered", "Status"])

    for student in students:
        data.append([f"{student.first_name} {student.middle_name or ''} {student.last_name}", student.email, student.course1, student.time_received, student.status])

    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),

        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))

    elements.append(Paragraph("<b>List of Student Applications</b>", styleN))
    elements.append(Spacer(1, 12))
    elements.append(table)

    doc.build(elements)

    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)

    return response

def student_community(request):
    success_message = ""
    feedback_form = FeedbackForm()
    
    if request.method == 'POST':
        feedback_form = FeedbackForm(request.POST)

        if feedback_form.is_valid():
            feedback_form.save()
            success_message = "Feedback Submitted Successfully!"
            messages.success(request, success_message)
            return redirect('student_community')  # Redirect to the same page after successful submission
        else:
            messages.error(request, "Form submission failed. Please check the data.")
    
    studcom = Feedback.objects.all()
    studans = StudentAnswer.objects.all()

    context = {
        'feedback_form': feedback_form,
        'success_message': success_message,
        'studcom': studcom,
        'studans': studans,
    }

    return render(request, 'student_community.html', context)
  
def submit_answer(request):
    sucess_message = ""
    subans_form = StudentAnswerForm()

    if request.method == 'POST':
        subans_form = StudentAnswerForm(request.POST)

        if subans_form.is_valid():
            subans_form.save()
            success_message = "Answer Submitted Successfully!"
            messages.success(request, success_message)
            return redirect('student_community')
        else:
            messages.error(request, "Form submission failed. Please check the data.")

    studans = StudentAnswer.objects.all()
    studcom = Feedback.objects.all()

    context = {
        'subans_form': subans_form,
        'success_message': success_message,
        'studans': studans,
        'studcom': studcom,
    }

    return render(request, 'student_community.html', context)

#Prediction for Recommending
