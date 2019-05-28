from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from ..models import CandidateSlot, InterviewerSlot
from .factories import (
    UserFactory, InterviewFactory, CandidateSlotFactory, InterviewerSlotFactory
)
from datetime import datetime
import factory.random
import json


class CreateCandidateSlotTest(TestCase):

    def setUp(self):
        factory.random.reseed_random('chemondis')
        self.client = APIClient()
        self.interview = InterviewFactory.create()

    def test_success(self):
        response = self.client.post(
            '/api/v1/interviews/{}/slots/'.format(self.interview.id),
            {'slots': [{'date': '2000-01-01 10:00'}]},
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(CandidateSlot.objects.count(), 1)

    def test_slots_taken(self):
        CandidateSlotFactory.create(
            date=datetime(2000, 1, 1, 10, 0),
            interview=self.interview
        )
        response = self.client.post(
            '/api/v1/interviews/{}/slots/'.format(self.interview.id),
            {'slots': [{'date': '2000-01-01 10:00'}]},
        )
        content = json.loads(response.content)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(content.get('date'), ['Slot(s) already taken.'])

    def test_invalid_date(self):
        response = self.client.post(
            '/api/v1/interviews/{}/slots/'.format(self.interview.id),
            {'slots': [{'date': '2000-01-01 10:05'}]},
        )
        content = json.loads(response.content)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            content.get('slots')[0].get('date'),
            ['Datetime must be on the hour.'])


class CreateInterviewerSlotTest(TestCase):

    def setUp(self):
        factory.random.reseed_random('chemondis')
        self.user = UserFactory.create()
        token = Token.objects.create(user=self.user)
        self.client = APIClient(HTTP_AUTHORIZATION='Token ' + token.key)
        self.interview = InterviewFactory.create()

    def test_interviewer_success(self):
        response = self.client.post(
            '/api/v1/interviews/{}/slots/'.format(self.interview.id), {
                'slots': [{'date': '2000-01-01 10:00'}]
            }
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(InterviewerSlot.objects.count(), 1)

    def test_slots_taken(self):
        InterviewerSlotFactory.create(
            date=datetime(2000, 1, 1, 10, 0),
            interview=self.interview,
            user=self.user
        )
        response = self.client.post(
            '/api/v1/interviews/{}/slots/'.format(self.interview.id), {
                'slots': [{'date': '2000-01-01 10:00'}]
            }
        )
        content = json.loads(response.content)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(content.get('date'), ['Slot(s) already taken.'])

    def test_invalid_date(self):
        response = self.client.post(
            '/api/v1/interviews/{}/slots/'.format(self.interview.id), {
                'slots': [{'date': '2000-01-01 10:05'}]
            }
        )
        content = json.loads(response.content)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            content.get('slots')[0].get('date'),
            ['Datetime must be on the hour.'])


class ListSlotTest(TestCase):

    def setUp(self):
        factory.random.reseed_random('chemondis')
        self.client = APIClient()
        self.interview = InterviewFactory.create()
        CSF = CandidateSlotFactory
        CSF.create(interview=self.interview, date=datetime(2000, 1, 1, 10, 0))
        CSF.create(interview=self.interview, date=datetime(2000, 1, 1, 11, 0))
        CSF.create(interview=self.interview, date=datetime(2000, 1, 1, 12, 0))

    def test_no_match(self):
        response = self.client.get(
            '/api/v1/interviews/{}/slots/'.format(self.interview.id)
        )
        content = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(content.get('slots')), 0)

    def test_single_match(self):
        user1 = UserFactory.create()
        user2 = UserFactory.create()
        InterviewerSlotFactory.create(
            interview=self.interview,
            date=datetime(2000, 1, 1, 12, 0),
            user=user1
        )
        InterviewerSlotFactory.create(
            interview=self.interview,
            date=datetime(2000, 1, 1, 12, 0),
            user=user2
        )

        response = self.client.get(
            '/api/v1/interviews/{}/slots/'.format(self.interview.id)
        )

        content = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(content.get('slots')), 1)
        self.assertEqual(content.get('slots')[0], {
            'date': '2000-01-01T12:00:00',
            'interviewers': [user1.id, user2.id]
        })

    def test_multiple_match(self):
        user1 = UserFactory.create()
        user2 = UserFactory.create()
        InterviewerSlotFactory.create(
            interview=self.interview,
            date=datetime(2000, 1, 1, 11, 0),
            user=user1
        )
        InterviewerSlotFactory.create(
            interview=self.interview,
            date=datetime(2000, 1, 1, 11, 0),
            user=user2
        )
        InterviewerSlotFactory.create(
            interview=self.interview,
            date=datetime(2000, 1, 1, 12, 0),
            user=user2
        )

        response = self.client.get(
            '/api/v1/interviews/{}/slots/'.format(self.interview.id)
        )

        content = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(content.get('slots')), 2)
        self.assertEqual(content.get('slots')[0], {
            'date': '2000-01-01T11:00:00',
            'interviewers': [user1.id, user2.id]
        })
        self.assertEqual(content.get('slots')[1], {
            'date': '2000-01-01T12:00:00',
            'interviewers': [user2.id]
        })
