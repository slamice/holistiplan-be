from rest_framework import generics, permissions, renderers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import status

from .models import Snippet, AppUser as User
from .permissions import IsOwnerOrReadOnly
from .serializers import SnippetSerializer, UserSerializer

import logging

logger = logging.getLogger(__name__)


class SnippetHighlight(generics.GenericAPIView):
    queryset = Snippet.objects.all()
    renderer_classes = (renderers.StaticHTMLRenderer,)

    def get(self, request, *args, **kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)


@api_view(["GET"])
def api_root(request, format=None):
    return Response(
        {
            "users": reverse("user-list", request=request, format=format),
            "snippets": reverse("snippet-list", request=request, format=format),
        }
    )


class SnippetList(generics.ListCreateAPIView):
    serializer_class = SnippetSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        result = None
        try:
            result = Snippet.objects.all()
        except Exception as e:
            breakpoint()
            logging.warning(f"Could not find Snippet objects: {e}")

        return result

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class SnippetDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = SnippetSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly,
    )

    def get_queryset(self):
        result = None
        try:
            result = Snippet.objects.first()
        except Exception as e:
            breakpoint()
            logging.warning(f"Could not find Snippet objects: {e}")

        return result


class UserList(generics.ListAPIView):
    serializer_class = UserSerializer

    def get_queryset(self):
        breakpoint()
        return User.objects.all()


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserCreate(generics.ListAPIView):
    """
    Create a user
    - This method is only allowed by the staff
    """

    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        # Allow only staff to create users
        if not request.user.is_staff:
            return Response(
                {"detail": "You do not have permission to perform this action."},
                status=status.HTTP_403_FORBIDDEN,
            )
        # Your user creation logic here
        return Response({"detail": "User created successfully."})


class UserDelete(generics.DestroyAPIView):
    """
    Only allow soft deletes
    If a user is deleted it should be filtered from all views of any non-staff user
    """

    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def delete(self, request, *args, **kwargs):
        breakpoint()
        # Restrict DELETE method to staff only, only soft deletes
        if not request.user.is_staff:
            return Response(
                {"detail": "You do not have permission to perform this action."},
                status=status.HTTP_403_FORBIDDEN,
            )
        return super().destroy(request, *args, **kwargs)
