"""
Forms for custom extra fields.
"""

import re

from django import forms
from django.forms import ModelForm

from custom_extra_fields.models import CustomExtraFields


def validate_nickname(value: str) -> None:
    """
    Validate the nickname for realistic constraints.
    """
    # Only allow alphanumeric characters, underscores, and hyphens
    if not re.match(r"^[a-zA-Z0-9_-]+$", value):
        raise forms.ValidationError(
            "Nickname can only contain letters, numbers, underscores, and hyphens."
        )

    # Cannot be only numbers
    if value.isdigit():
        raise forms.ValidationError("Nickname cannot be only numbers.")


class CustomExtraFieldsForm(ModelForm):
    """
    Form that represents user extra info and is compatible with edX's FormDescription system.

    Adding a field as 'required' will make it mandatory for the user to fill it in, and
    and will show it in the registration form.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Text
        self.fields["nickname"].help_text = "Enter your nickname."
        self.fields["nickname"].min_length = 3
        self.fields["nickname"].max_length = 50
        self.fields["nickname"].required = True
        self.fields["nickname"].validators = [validate_nickname]
        self.fields["nickname"].restrictions = {
            "min_length": 3,
            "max_length": 50,
        }
        self.fields["nickname"].error_messages = {
            "required": "Please enter a nickname to identify you.",
        }

        # Text area
        self.fields["interests"].help_text = "Tell us about your hobbies and interests."
        self.fields["interests"].required = True
        self.fields["interests"].error_messages = {
            "required": "Please tell us about your interests.",
        }

        # Check box
        self.fields["wants_newsletter"].label = "Subscribe to newsletter?"

        # Select
        self.fields[
            "favorite_language"
        ].help_text = "Pick your preferred programming language."
        self.fields["favorite_language"].required = True

    class Meta:
        model = CustomExtraFields
        fields = [
            "nickname",
            "interests",
            "wants_newsletter",
            "favorite_language",
        ]

        serialization_options = {
            "nickname": {
                "default": "Funny Nickname",
            },
        }
