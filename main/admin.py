from django.contrib import admin

# Register your models here.
from .models import Student, Faculty, Course, Department, Assignment, Announcement, Feedback, StudentAnswer
class StudentAdmin(admin.ModelAdmin):
    readonly_fields = ('formatted_time_received',)

    def formatted_time_received(self, obj):
        return obj.time_received.strftime("%Y-%m-%d | %H:%M:%S")
    formatted_time_received.short_description = "Local Time"

admin.site.register(Feedback)
admin.site.register(StudentAnswer)   
admin.site.register(Student, StudentAdmin)
admin.site.register(Faculty)
admin.site.register(Course)
admin.site.register(Department)
admin.site.register(Assignment)
admin.site.register(Announcement)