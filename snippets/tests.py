from django.test import TestCase
from rest_framework.test import APIClient

from snippets.factories import SnippetFactory, UserFactory
from snippets.models import Snippet
import pytest

from snippets.views import SnippetList


class BaseApiTest:
    @pytest.fixture(autouse=True)
    def setup_class(self):
        # Set up the API client for the test class
        self.api_client = APIClient()


# @pytest.mark.django_db
# class TestSnippetList(BaseApiTest):
#     def test__get_queryset__no_objects(self):
#         """Test that the view returns no snippets."""
#         response = self.api_client.get("/snippets/")
#         assert response.data["results"] == []

#     def test__get_queryset(self):
#         """Test that the view returns no snippets."""
#         user = UserFactory.create()
#         SnippetFactory.create(owner=user)
#         response = self.api_client.get("/snippets/")
#         assert len(response.data["results"]) == 1


@pytest.mark.django_db
class TestUserDelete(BaseApiTest):
    def test__delete__not_staff(self):
        """Test that the view returns no snippets."""
        user = UserFactory()
        # self.api_client.credentials(HTTP_AUTHORIZATION="Token " + self.token_user1.key)

        response = self.api_client.delete(f"/users/{user.id}/delete/")
        breakpoint()
        assert response.data["results"] == []
