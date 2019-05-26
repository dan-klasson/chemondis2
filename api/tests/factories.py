import factory
from .. import models
from django.contrib.auth.models import User
from datetime import datetime


class UserFactory(factory.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Faker('name')
    email = factory.Faker('email')
    password = factory.PostGenerationMethodCall('set_password', 'password')


class InterviewFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.Interview

    candidate_name = factory.Faker('name')
    candidate_email = factory.Faker('email')


class CandidateSlotFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.CandidateSlot

    date = factory.Faker(
        'date_between',
        start_date=datetime(2000, 1, 1, 10, 0)
    )
    interview = factory.SubFactory(InterviewFactory)


class InterviewerSlotFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.InterviewerSlot

    user = factory.SubFactory(UserFactory)
    interview = factory.SubFactory(InterviewFactory)
