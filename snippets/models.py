from django.utils import timezone
from django.db import models
from pygments import highlight
from pygments.formatters.html import HtmlFormatter
from pygments.lexers import get_all_lexers, get_lexer_by_name
from pygments.styles import get_all_styles
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import BaseUserManager


LEXERS = [item for item in get_all_lexers() if item[1]]
LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])
STYLE_CHOICES = sorted((item, item) for item in get_all_styles())


class AppUserManager(BaseUserManager):
    def get_queryset(self):
        # Override for soft delete users
        return super().get_queryset().filter(is_deleted=False)

    def create_user(self, username, email=None, password=None, **extra_fields):
        """
        Create and return a regular user with an email and password.
        """
        if not username:
            raise ValueError("The Username field must be set")
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        """
        Create and return a superuser with an email, password, and additional fields.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(username, email, password, **extra_fields)

    def get_by_natural_key(self, username):
        """
        Retrieve a user by their username.
        """
        return self.get(username=username)


class AppUser(AbstractUser):
    is_deleted = models.BooleanField(default=False)

    objects = AppUserManager()  # type: ignore
    all_objects = models.Manager()  # type: ignore

    def delete(self):
        self.is_deleted = True
        self.save()


class Snippet(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=True, default="")
    code = models.TextField()
    linenos = models.BooleanField(default=False)
    language = models.CharField(
        choices=LANGUAGE_CHOICES, default="python", max_length=100
    )
    style = models.CharField(choices=STYLE_CHOICES, default="friendly", max_length=100)
    owner = models.ForeignKey(
        AppUser, related_name="snippets", on_delete=models.CASCADE
    )
    highlighted = models.TextField()

    class Meta:
        ordering = ("created",)

    def save(self, *args, **kwargs):
        """
        Use the `pygments` library to create a highlighted HTML
        representation of the code snippet.
        """
        lexer = get_lexer_by_name(self.language)
        linenos = "table" if self.linenos else False
        options = {"title": self.title} if self.title else {}
        formatter = HtmlFormatter(
            style=self.style, linenos=linenos, full=True, **options
        )
        self.highlighted = highlight(self.code, lexer, formatter)
        super(Snippet, self).save(*args, **kwargs)

    def __str__(self):
        return self.title
