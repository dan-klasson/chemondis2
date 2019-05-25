import factory
from . import models
from django.contrib.auth.models import User


class UserFactory(factory.DjangoModelFactory):
    class Meta:
        model = User

    email = factory.Faker('email')
    password = factory.PostGenerationMethodCall('set_password', 'password')
