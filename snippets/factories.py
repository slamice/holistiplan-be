import factory
from .models import Snippet, AppUser
from factory.django import DjangoModelFactory


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = AppUser

    username = factory.Faker("user_name")  # Faker generates a random username
    email = factory.Faker("email")  # Faker generates a random email
    password = factory.PostGenerationMethodCall("set_password", "defaultpassword")


class SnippetFactory(DjangoModelFactory):
    class Meta:
        model = Snippet
