"""
Database models for custom_extra_fields.
"""

from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class CustomExtraFields(models.Model):
    """
    Model that extends the User model with custom fields.
    """

    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)

    nickname = models.CharField(
        blank=True,
        max_length=50,
        validators=[MinLengthValidator(3)],
        verbose_name=_("Nickname"),
    )

    interests = models.TextField(
        blank=True,
        verbose_name=_("Interests"),
        help_text=_("Tell us about your hobbies and interests."),
    )

    wants_newsletter = models.BooleanField(
        default=False,
        verbose_name=_("Subscribe to newsletter"),
    )

    favorite_language = models.CharField(
        blank=True,
        max_length=50,
        choices=[
            ("python", "Python"),
            ("javascript", "JavaScript"),
            ("java", "Java"),
            ("go", "Go"),
        ],
        verbose_name=_("Favorite programming language"),
    )

    def __str__(self):
        """
        Get a string representation of this model instance.
        """
        return f"<CustomExtraFields, ID: {self.id}>"
