from rest_framework.fields import CurrentUserDefault
from rest_framework_json_api import serializers

from afi_backend.exams.models import Answer, Exam, Question, TestAssignment, Progress


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = [
            'id',
            'text',
            'correct',
        ]


class QuestionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(read_only=True, many=True)

    class Meta:
        model = Question
        fields = [
            'text',
            'answers',
        ]


class ExamSerializer(serializers.ModelSerializer):
    test_assignment_id = serializers.IntegerField()
    questions = serializers.SerializerMethodField()
    results = serializers.SerializerMethodField()

    class Meta:
        model = Exam
        fields = [
            'id',
            'test_assignment_id',
            'user',
            'results',
            'questions',
        ]
        read_only_fields = [
            'user',
            'progress'
        ]

    def get_results(self, obj):
        return obj.test_results()

    def get_questions(self, obj):
        # todo serialize many questions
        serializer = QuestionSerializer(obj.test_assignment.questions.all(), many=True)

        return serializer.data

    def create(self, validated_data):
        from afi_backend.exams.api.serializers import QuestionSerializer
        # Create Exam using test_assignment_id
        test_assignment = TestAssignment.objects.get(id=validated_data['test_assignment_id'])
        exam = Exam.objects.create(user=self.context['request'].user, test_assignment=test_assignment)

        return exam


class TestAssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestAssignment
        fields = [
            'id'
        ]


class ExamProgressSerializer(serializers.Serializer):
    answer_id = serializers.IntegerField(source='chosen_aswers.id', read_only=True)
    chosen_answers = AnswerSerializer(read_only=True, many=True)

    class Meta:
        model = Progress
        fields = [
            'answer_id',
            'chosen_answers',

        ]
