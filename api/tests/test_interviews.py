from django.test import TestCase
from rest_framework.test import APIClient
from .factories import InterviewFactory
from ..models import Interview
import factory.random
import json


class InterviewTestCase(TestCase):

    def setUp(self):
        factory.random.reseed_random('chemondis')
        self.client = APIClient()

    def test_retrieve(self):
        obj = InterviewFactory.create()
        response = self.client.get('/api/v1/interviews/{}/'.format(obj.id))
        data = json.loads(response.content)
        self.assertEqual(data['candidate_name'], 'Kari Patterson')
        self.assertEqual(data['candidate_email'], 'paulpadilla@williams.org')

    def test_list(self):
        InterviewFactory.create_batch(size=5)
        response = self.client.get('/api/v1/interviews/')
        data = json.loads(response.content)

        self.assertEqual(len(data), 5)
        self.assertEqual(data[0]['candidate_name'], 'Kari Patterson')
        self.assertEqual(
            data[0]['candidate_email'], 'paulpadilla@williams.org'
        )

    def test_create(self):
        self.client.post('/api/v1/interviews/', {
            'candidate_name': 'jane doe',
            'candidate_email': 'jane@example.com'
        })
        obj = Interview.objects.first()
        self.assertEqual(obj.candidate_name, 'jane doe')
        self.assertEqual(obj.candidate_email, 'jane@example.com')

    def test_create__empty(self):
        response = self.client.post('/api/v1/interviews/', {
            'candidate_name': '',
            'candidate_email': ''
        })
        data = json.loads(response.content)
        blank = ['This field may not be blank.']
        self.assertEqual(data.get('candidate_name'), blank)
        self.assertEqual(data.get('candidate_email'), blank)

    def test_create__null(self):
        response = self.client.post('/api/v1/interviews/')
        data = json.loads(response.content)
        required = ['This field is required.']
        self.assertEqual(data.get('candidate_name'), required)
        self.assertEqual(data.get('candidate_email'), required)

    def test_create__invalid_email(self):
        response = self.client.post('/api/v1/interviews/', {
            'candidate_name': 'jane',
            'candidate_email': 'invalid'
        })
        data = json.loads(response.content)
        self.assertEqual(
            data.get('candidate_email'),
            ['Enter a valid email address.']
        )

    def test_update(self):
        obj = InterviewFactory.create()
        self.client.put(
            '/api/v1/interviews/{}/'.format(obj.id),
            {
                'candidate_name': 'jane doe',
                'candidate_email': 'jane@example.com',
            }
        )
        obj = Interview.objects.first()
        self.assertEqual(obj.candidate_name, 'jane doe')
        self.assertEqual(obj.candidate_email, 'jane@example.com')

    def test_delete(self):
        obj = InterviewFactory.create()
        self.assertEqual(Interview.objects.count(), 1)
        self.client.delete('/api/v1/interviews/{}/'.format(obj.id))
        self.assertEqual(Interview.objects.count(), 0)
