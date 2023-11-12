from django.urls import path
from . import views

urlpatterns = [

    path('', views.std_login, name='std_login'),
    path('my/', views.myCourses, name='myCourses'),
    path('facultyCourses/', views.facultyCourses, name='facultyCourses'),
    path('login/', views.std_login, name='std_login'),
    path('logout/', views.std_logout, name='std_logout'),
    path('my/<int:code>/', views.course_page, name='course'),
    path('profile/<str:id>/', views.profile, name='profile'),
    path('facultyProfile/<str:id>/', views.profile, name='profile_faculty'),
    path('faculty/<int:code>/', views.course_page_faculty, name='faculty'),


     #For Announcement BSIT section start
    path('addAnnouncement/<int:code>/',
         views.addAnnouncement, name='addAnnouncement'),
    path('announecement/<int:code>/<int:id>/',
         views.deleteAnnouncement, name='deleteAnnouncement'),
    path('edit/<int:code>/<int:id>/',
         views.editAnnouncement, name='editAnnouncement'),
    path('update/<int:code>/<int:id>/',
         views.updateAnnouncement, name='updateAnnouncement'),
     #For Announcement BSIT section ends

    path('addAssignment/<int:code>/', views.addAssignment, name='addAssignment'),
    path('assignment/<int:code>/<int:id>/',
         views.assignmentPage, name='assignmentPage'),
    path('assignments/<int:code>/', views.allAssignments, name='allAssignments'),
    path('student-assignments/<int:code>/',
         views.allAssignmentsSTD, name='student-assignments'),
    path('addSubmission/<int:code>/<int:id>/',
         views.addSubmission, name='addSubmission'),
    path('submission/<int:code>/<int:id>/',
         views.viewSubmission, name='submission'),
    path('gradeSubmission/<int:code>/<int:id>/<int:sub_id>',
         views.gradeSubmission, name='gradeSubmission'),

    path('course-material/<int:code>/',
         views.addCourseMaterial, name='addCourseMaterial'),
    path('course-material/<int:code>/<int:id>/',
         views.deleteCourseMaterial, name='deleteCourseMaterial'),
    path('courses/', views.courses, name='courses'),
    path('departments/', views.departments, name='departments'),
    path('access/<int:code>/', views.access, name='access'),
    path('changePasswordPrompt/', views.changePasswordPrompt,
         name='changePasswordPrompt'),
    path('changePhotoPrompt/', views.changePhotoPrompt, name='changePhotoPrompt'),
    path('changePassword/', views.changePassword, name='changePassword'),
    path('changePasswordFaculty/', views.changePasswordFaculty,
         name='changePasswordFaculty'),
    path('changePhoto/', views.changePhoto, name='changePhoto'),
    path('changePhotoFaculty/', views.changePhotoFaculty,
         name='changePhotoFaculty'),
    path('search/', views.search, name='search'),
    path('error/', views.error, name='error'),
    
    path('admission/', views.admission_index, name='admission_index'),

    path('register_user.html', views.register_user, name='register_user'),

    path('notifications/', views.notifications, name='notifications'),

    path('student_profile.html/<str:id>/', views.student_profile, name='student_profile'),

    path('home.html', views.home, name='home'),
    
    path('generate_pdf/', views.generate_pdf, name='generate_pdf'),

    path('student-community/', views.student_community, name='student_community'),
    
    path('submit_answer/', views.submit_answer, name='submit_answer'),
]