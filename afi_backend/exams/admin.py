from django.contrib import admin
from afi_backend.exams.models import Answer, Question, TestAssignment


class AnswerInline(admin.TabularInline):
    model = Answer


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    inlines = [
        AnswerInline,
    ]


@admin.register(TestAssignment)
class TestAssignmentAdmin(admin.ModelAdmin):
    fields = ['questions', 'content_type', 'object_id']
