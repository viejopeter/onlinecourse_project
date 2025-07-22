from django.contrib import admin
from .models import Course, Lesson, Instructor, Learner, Question, Choice, Submission

# ===============================
# Inline Admin Classes
# ===============================

# Show related Choices inline when editing a Question
class ChoiceInline(admin.StackedInline):
    model = Choice
    extra = 2  # Show 2 extra empty Choice fields by default

# Show related Questions inline when editing a Lesson
# It is not used for now
class QuestionInline(admin.StackedInline):
    model = Question
    extra = 2  # Show 2 extra empty Question fields by default

# Show related Lessons inline when editing a Course
class LessonInline(admin.StackedInline):
    model = Lesson
    extra = 5  # Show 5 extra empty Lesson fields by default

# ===============================
# Model Admin Customizations
# ===============================

# Customize how Course appears in the admin
class CourseAdmin(admin.ModelAdmin):
    inlines = [LessonInline]  # Show Lessons inline in the Course form
    list_display = ('name', 'pub_date')  # Display Course name and publication date
    list_filter = ['pub_date']  # Enable sidebar filter for pub_date
    search_fields = ['name', 'description']  # Enable search by name and description

# Customize how Lesson appears in the admin
class LessonAdmin(admin.ModelAdmin):
    list_display = ['title']  # Display Lesson title in the list view

# Customize how Question appears in the admin
class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]  # Show Choices inline in the Question form
    list_display = ['content']  # Display Question content in the list view

# ===============================
# Register Models in Admin Site
# ===============================

# Register models with their customized admin classes
admin.site.register(Course, CourseAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Question, QuestionAdmin)

# Register models using default admin configuration
admin.site.register(Instructor)
admin.site.register(Learner)
admin.site.register(Choice)
admin.site.register(Submission)
