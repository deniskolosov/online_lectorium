from rest_framework_json_api import serializers
from rest_framework.fields import CurrentUserDefault
from afi_backend.exams.models import Exam, Question, Answer, TestAssignment


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = [
            'text',
            'correct',
        ]


class QuestionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(read_only=True, many=True)

    class Meta:
        model = Question
        fields = [
            'text',
            'answer',
        ]


class ExamSerializer(serializers.ModelSerializer):
    test_assignment_id = serializers.IntegerField()
    included_serializers = {
        'questions': QuestionSerializer
    }

    class Meta:
        model = Exam
        fields = [
            'test_assignment_id',
            'user',
        ]
        read_only_fields = [
            'user',
            'result',
            'progress'
        ]

    def create(self, validated_data):
        # Create Exam using test_assignment_id
        test_assignment = TestAssignment.objects.get(id=validated_data['test_assignment_id'])
        exam = Exam.objects.create(user=self.context['request'].user, test_assignment=test_assignment)

        return exam
