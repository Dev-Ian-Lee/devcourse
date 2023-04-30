from django.urls import reverse
from django.utils import timezone
from django.test import TestCase
from django.contrib.auth.models import User
from polls_api.serializers import QuestionSerializer, VoteSerializer
from polls.models import Question, Choice, Vote
from rest_framework import status
from rest_framework.test import APITestCase

class QuestionListTest(APITestCase):
    def setUp(self):
        self.question_data = {"question_text": "some question"}
        self.url = reverse("question-list")

    # Question을 생성하는 요청을 보냈을 때 잘 처리되는지 테스트
    def test_create_question(self):
        user = User.objects.create(username = "testuser", password = "testpass")

        # 강제 인증
        self.client.force_authenticate(user = user)
        response = self.client.post(self.url, self.question_data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Question.objects.count(), 1)

        question = Question.objects.first()
        self.assertEqual(question.question_text, self.question_data["question_text"])
        self.assertLess((timezone.now() - question.pub_date).total_seconds(), 1)

    # 인증되지 않은 사용자가 POST 요청을 보낼 경우 403에러가 잘 발생하는지 테스트
    def test_create_question_without_authentication(self):
        response = self.client.post(self.url, self.question_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # 테스트 목록을 요청했을 때 잘 처리되는지 테스트
    def test_list_question(self):
        question = Question.objects.create(question_text = "Qeustion1")
        choice = Choice.objects.create(question = question, choice_text = "choice1")
        Question.objects.create(question_text = "Qeustion2")
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]["choices"][0]["choice_text"], choice.choice_text)

class VoteSerializerTest(TestCase):

    # 각 테스트 메서드가 실행되기 전에 실행되는 설정 메서드
    # 각 테스트 메서드마다 새로운 데이터 생성
    def setUp(self):
        self.user = User.objects.create(username = "testuser")

        self.question = Question.objects.create(
            question_text = "abc",
            owner = self.user
        )

        self.choice = Choice.objects.create(
            question = self.question,
            choice_text = "1"
        )

    # 새로운 Vote 객체가 잘 생성되는지 테스트
    def test_vote_serializer(self):
        data = {
            "question": self.question.id,
            "choice": self.choice.id,
            "voter": self.user.id
        }

        serializer = VoteSerializer(data = data)
        self.assertTrue(serializer.is_valid())

        vote = serializer.save()
        self.assertEqual(vote.question, self.question)
        self.assertEqual(vote.choice, self.choice)
        self.assertEqual(vote.voter, self.user)

    # User가 이미 투표한 상태에서 또 투표하려고 할 때 ValidationError가 잘 발생하는지 테스트
    def test_vote_serializer_with_duplicate_vote(self):
        choice1 = Choice.objects.create(
            question = self.question,
            choice_text = "2"
        )

        Vote.objects.create(question = self.question, choice = self.choice, voter = self.user)

        data = {
            "question": self.question.id,
            "choice": self.choice.id,
            "voter": self.user.id
        }

        serializer = VoteSerializer(data = data)
        self.assertFalse(serializer.is_valid())

    # Question과 Choice의 조합이 맞지 않을 경우 ValidationError가 잘 발생하는지 테스트
    def test_vote_serializer_with_unmatched_question_and_choice(self):
        question2 = Question.objects.create(
            question_text = "abc",
            owner = self.user
        )

        choice2 = Choice.objects.create(
            question = question2,
            choice_text = "1"
        )

        data = {
            "question": self.question.id,
            "choice": choice2.id,
            "voter": self.user.id
        }

        serializer = VoteSerializer(data = data)
        self.assertFalse(serializer.is_valid())

# Create your tests here.
class QuestionSerializerTestCase(TestCase):
    # QuestionSerializer의 is_valid() 메서드와 save() 메서드가 제대로 동작하는지 테스트
    def test_with_valid_data(self):
        serializer = QuestionSerializer(data = {"question_text": "abc"})
        self.assertEqual(serializer.is_valid(), True)

        new_question = serializer.save()
        self.assertIsNotNone(new_question.id)

    def test_with_invalid_test(self):
        serializer = QuestionSerializer(data = {"question_text": ""})
        self.assertEqual(serializer.is_valid(), False)